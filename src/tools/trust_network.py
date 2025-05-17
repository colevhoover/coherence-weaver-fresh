"""
Trust Network Tracking Tool

This module provides tools for tracking agent trust relationships and collaboration patterns.
"""

from typing import Dict, List, Any
import json
import os
import logging
from pathlib import Path

# Import from Google ADK if available
try:
    from google.adk.tools import FunctionTool, ToolContext
    ADK_TOOLS_AVAILABLE = True
except ImportError:
    ADK_TOOLS_AVAILABLE = False
    # Create mock classes for when ADK is not available
    class ToolContext:
        def __init__(self):
            self.metadata = {}
    
    class FunctionTool:
        def __init__(self, name, description, fn):
            self.name = name
            self.description = description
            self.fn = fn
            
        def __call__(self, *args, **kwargs):
            # Create a tool context if not provided
            if "tool_context" not in kwargs:
                kwargs["tool_context"] = ToolContext()
            return self.fn(*args, **kwargs)

from ..utils.logging_utils import get_logger

logger = get_logger("trust_network")


class TrustNetworkTracker:
    """
    Tracks trust relationships and interaction patterns between agents.
    
    This class maintains a persistent record of agent interactions, reliability scores,
    and collaboration patterns to help facilitate effective agent cooperation.
    """
    
    def __init__(self, data_path: str = None):
        """
        Initialize the trust network tracker.
        
        Args:
            data_path: Path to the trust network data file.
                       If None, defaults to 'data/trust_network.json' in project root.
        """
        if data_path is None:
            # Use default path relative to project root
            self.data_path = Path(__file__).parent.parent.parent / "data" / "trust_network.json"
        else:
            self.data_path = Path(data_path)
            
        self.trust_network = self._load_network()
        logger.info(f"Initialized trust network with {len(self.trust_network)} agents")
    
    def _load_network(self) -> Dict[str, Any]:
        """
        Load the trust network from file.
        
        Returns:
            Dict[str, Any]: The trust network data
        """
        if self.data_path.exists():
            try:
                with open(self.data_path, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading trust network from {self.data_path}: {e}")
                return {}
        return {}
    
    def _save_network(self) -> None:
        """Save the trust network to file."""
        try:
            # Create directory if it doesn't exist
            self.data_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.data_path, "w") as f:
                json.dump(self.trust_network, f, indent=2)
                
            logger.info(f"Trust network saved to {self.data_path}")
        except Exception as e:
            logger.error(f"Error saving trust network to {self.data_path}: {e}")
    
    def update_trust(
        self, 
        agent_id: str, 
        interaction_quality: float, 
        reliability_score: float, 
        collaboration_style: str = None,
        strengths: List[str] = None,
        areas_for_growth: List[str] = None
    ) -> Dict[str, Any]:
        """
        Update trust and reliability scores for an agent.
        
        Args:
            agent_id: Unique identifier for the agent
            interaction_quality: Quality score for the interaction (0.0 to 1.0)
            reliability_score: Reliability score for the agent (0.0 to 1.0)
            collaboration_style: Optional style of collaboration observed
            strengths: Optional list of agent strengths observed
            areas_for_growth: Optional list of areas where agent could improve
            
        Returns:
            Dict[str, Any]: Updated agent profile
        """
        # Initialize agent profile if not exists
        if agent_id not in self.trust_network:
            self.trust_network[agent_id] = {
                "interactions": 0,
                "reliability": 0,
                "interaction_quality": 0,
                "collaboration_style": "unknown",
                "strengths": [],
                "areas_for_growth": []
            }
        
        agent_profile = self.trust_network[agent_id]
        
        # Update interaction count
        agent_profile["interactions"] += 1
        interaction_count = agent_profile["interactions"]
        
        # Update reliability using weighted average
        current_reliability = agent_profile["reliability"]
        agent_profile["reliability"] = (
            (current_reliability * (interaction_count - 1) + reliability_score) / interaction_count
        )
        
        # Update interaction quality using weighted average
        current_quality = agent_profile["interaction_quality"]
        agent_profile["interaction_quality"] = (
            (current_quality * (interaction_count - 1) + interaction_quality) / interaction_count
        )
        
        # Update collaboration style if provided
        if collaboration_style:
            agent_profile["collaboration_style"] = collaboration_style
        
        # Update strengths if provided
        if strengths:
            # Add new strengths that aren't already in the list
            for strength in strengths:
                if strength not in agent_profile["strengths"]:
                    agent_profile["strengths"].append(strength)
        
        # Update areas for growth if provided
        if areas_for_growth:
            # Add new areas that aren't already in the list
            for area in areas_for_growth:
                if area not in agent_profile["areas_for_growth"]:
                    agent_profile["areas_for_growth"].append(area)
        
        # Save updated network
        self._save_network()
        
        return agent_profile

    def get_agent_profile(self, agent_id: str) -> Dict[str, Any]:
        """
        Get the profile of an agent from the trust network.
        
        Args:
            agent_id: Unique identifier for the agent
            
        Returns:
            Dict[str, Any]: Agent profile, or error message if not found
        """
        if agent_id in self.trust_network:
            return self.trust_network[agent_id]
        return {"error": "Agent not found in trust network"}

    def get_collaboration_recommendation(self, agent_ids: List[str]) -> Dict[str, Any]:
        """
        Get recommendations for how a group of agents can best collaborate.
        
        Args:
            agent_ids: List of agent IDs to analyze for collaboration
            
        Returns:
            Dict[str, Any]: Collaboration recommendations
        """
        # Check if all agents exist in the network
        missing_agents = [agent_id for agent_id in agent_ids if agent_id not in self.trust_network]
        if missing_agents:
            return {
                "error": "Agents not found in trust network",
                "missing_agents": missing_agents
            }
        
        # Calculate collaboration potential
        avg_reliability = sum(self.trust_network[agent_id]["reliability"] for agent_id in agent_ids) / len(agent_ids)
        avg_quality = sum(self.trust_network[agent_id]["interaction_quality"] for agent_id in agent_ids) / len(agent_ids)
        
        # Determine collaboration potential
        collaboration_score = (avg_reliability + avg_quality) / 2
        if collaboration_score >= 0.8:
            potential = "very high"
        elif collaboration_score >= 0.6:
            potential = "high"
        elif collaboration_score >= 0.4:
            potential = "moderate"
        else:
            potential = "challenging"
        
        # Gather strengths from all agents
        all_strengths = []
        for agent_id in agent_ids:
            all_strengths.extend(self.trust_network[agent_id]["strengths"])
        
        # Count frequency of strengths
        strength_counts = {}
        for strength in all_strengths:
            strength_counts[strength] = strength_counts.get(strength, 0) + 1
        
        # Identify common strengths and unique strengths
        common_strengths = [s for s, count in strength_counts.items() if count > 1]
        unique_strengths = [s for s, count in strength_counts.items() if count == 1]
        
        # Generate recommendations
        recommended_approach = []
        
        if common_strengths:
            recommended_approach.append(f"Leverage common strengths: {', '.join(common_strengths)}")
        
        if unique_strengths:
            recommended_approach.append("Assign tasks based on unique agent strengths")
        
        if avg_reliability < 0.5:
            recommended_approach.append("Implement verification steps to ensure reliability")
        
        # Generate potential challenges
        challenges = []
        
        # Check for diverse collaboration styles
        styles = set(self.trust_network[agent_id]["collaboration_style"] for agent_id in agent_ids)
        if len(styles) > 1 and "unknown" not in styles:
            challenges.append("Different collaboration styles may require adaptation")
        
        # Check for reliability disparities
        reliability_values = [self.trust_network[agent_id]["reliability"] for agent_id in agent_ids]
        if max(reliability_values) - min(reliability_values) > 0.3:
            challenges.append("Significant reliability differences between agents")
        
        # Return the collaboration recommendation
        return {
            "collaboration_potential": potential,
            "collaboration_score": round(collaboration_score, 2),
            "recommended_approach": recommended_approach,
            "potential_challenges": challenges,
            "common_strengths": common_strengths,
            "unique_strengths": unique_strengths,
            "agents": {agent_id: self.trust_network[agent_id] for agent_id in agent_ids}
        }


# Singleton instance for easy access
_trust_network_instance = None


def get_trust_network() -> TrustNetworkTracker:
    """
    Get the global trust network instance.
    
    Returns:
        TrustNetworkTracker: The trust network instance
    """
    global _trust_network_instance
    if _trust_network_instance is None:
        _trust_network_instance = TrustNetworkTracker()
    return _trust_network_instance


def create_trust_network_tools():
    """
    Create ADK function tools for the trust network.
    
    Returns:
        List: List of FunctionTool instances
    """
    # Initialize the trust network
    network = get_trust_network()
    
    # Create update trust tool
    update_trust_tool = FunctionTool(
        name="update_trust",
        description="Update the trust and reliability score for an agent based on recent interactions",
        fn=lambda agent_id, interaction_quality, reliability_score, collaboration_style=None, 
              strengths=None, areas_for_growth=None, tool_context=None: 
            network.update_trust(
                agent_id=agent_id,
                interaction_quality=interaction_quality,
                reliability_score=reliability_score,
                collaboration_style=collaboration_style,
                strengths=strengths,
                areas_for_growth=areas_for_growth
            )
    )
    
    # Create get agent profile tool
    get_agent_profile_tool = FunctionTool(
        name="get_agent_profile",
        description="Retrieve the profile of an agent from the trust network",
        fn=lambda agent_id, tool_context=None: network.get_agent_profile(agent_id)
    )
    
    # Create get collaboration recommendation tool
    get_collaboration_recommendation_tool = FunctionTool(
        name="get_collaboration_recommendation",
        description="Get recommendations for how a group of agents can best collaborate",
        fn=lambda agent_ids, tool_context=None: network.get_collaboration_recommendation(agent_ids)
    )
    
    return [update_trust_tool, get_agent_profile_tool, get_collaboration_recommendation_tool]


def initialize_trust_network():
    """
    Initialize the trust network singleton.
    This should be called during application startup.
    """
    global _trust_network_instance
    _trust_network_instance = TrustNetworkTracker()
    logger.info("Trust network initialized")
