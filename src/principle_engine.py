"""
Principle Engine Module

This module defines the PrincipleEngine class, which manages and applies 
participatory resilience principles within the Coherence Weaver agent system.
"""

from typing import Dict, List, Set, Any, Optional, Tuple, Union
import logging
import random
from datetime import datetime
import json
import os
from pathlib import Path

from .principles.participatory_resilience import (
    get_principle, 
    get_principles_by_domain, 
    get_related_principles,
    apply_principle_to_decision,
    apply_meta_principles,
    create_principle_guidance,
    get_recommended_principles_for_context,
    ALL_PRINCIPLES, 
    META_PRINCIPLES
)

# Initialize logging
logger = logging.getLogger("principle_engine")

class PrincipleEngine:
    """
    The PrincipleEngine manages and applies participatory resilience principles
    throughout the Coherence Weaver agent ecosystem.
    
    It serves as the central mechanism for principle-guided decision making,
    providing interfaces for:
    - Principle retrieval and relationship mapping
    - Context-appropriate principle application
    - Principle-based evaluations and recommendations
    - Balancing considerations across domains
    - Meta-principle application for system evolution
    """
    
    def __init__(
        self,
        config_path: Optional[str] = None,
        enable_caching: bool = True,
        default_domain_weights: Optional[Dict[str, float]] = None
    ):
        """
        Initialize a new PrincipleEngine instance.
        
        Args:
            config_path: Optional path to configuration file for principle settings
            enable_caching: Whether to enable caching for performance optimization
            default_domain_weights: Default weights for different domains
        """
        self.enable_caching = enable_caching
        self.default_domain_weights = default_domain_weights or {
            "Culture": 0.4,
            "Tech": 0.4,
            "Trade": 0.2
        }
        
        # Initialize caches
        self._principle_cache = {}
        self._guidance_cache = {}
        self._relationship_cache = {}
        
        # Load config if provided
        self.config = {}
        if config_path:
            self._load_config(config_path)
            
        # Initialize principle usage statistics
        self.principle_usage = {name: 0 for name in ALL_PRINCIPLES}
        self.principle_usage.update({name: 0 for name in META_PRINCIPLES})
        
        logger.info("PrincipleEngine initialized")
        
    def _load_config(self, config_path: str) -> None:
        """
        Load configuration from file.
        
        Args:
            config_path: Path to configuration file
        """
        try:
            with open(config_path, 'r') as f:
                self.config = json.load(f)
                
            # Apply config settings
            if 'domain_weights' in self.config and 'default' in self.config['domain_weights']:
                self.default_domain_weights = self.config['domain_weights']['default']
                
            logger.info(f"Loaded configuration from {config_path}")
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
    
    def create_guidance_for_task(
        self, 
        task_description: str,
        context: Optional[Dict[str, Any]] = None,
        domain_weights: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Create principle-based guidance for a task.
        
        Args:
            task_description: Description of the task
            context: Optional additional context for the task
            domain_weights: Optional custom domain weights
            
        Returns:
            Dictionary with principle-based guidance
        """
        # Use default weights if not provided
        domain_weights = domain_weights or self.default_domain_weights
        
        # Check cache if enabled
        cache_key = f"{task_description}:{json.dumps(domain_weights, sort_keys=True)}"
        if self.enable_caching and cache_key in self._guidance_cache:
            return self._guidance_cache[cache_key]
        
        # Generate guidance
        guidance = create_principle_guidance(task_description, domain_weights)
        
        # Update usage statistics
        for principle in guidance['primary_principles']:
            self.principle_usage[principle['name']] += 1
            
        # Cache result if enabled
        if self.enable_caching:
            self._guidance_cache[cache_key] = guidance
            
        return guidance
    
    def assess_alignment(
        self,
        agent_principles: Dict[str, Union[float, Dict[str, Any]]],
        threshold: float = 0.6
    ) -> Dict[str, Any]:
        """
        Assess an agent's principle alignment with the system's principles.
        
        Args:
            agent_principles: Dictionary of principles the agent aligns with
            threshold: Minimum score to consider principles aligned
            
        Returns:
            Dictionary with alignment assessment
        """
        alignment_scores = {}
        overall_alignment = 0.0
        aligned_principles = []
        misaligned_principles = []
        
        # Assess each principle the agent claims to align with
        for principle_name, alignment in agent_principles.items():
            # Get alignment score (either direct or from dict)
            score = alignment if isinstance(alignment, float) else alignment.get('score', 0.0)
            
            # Check if principle exists in our system
            principle = get_principle(principle_name)
            if principle:
                alignment_scores[principle_name] = score
                if score >= threshold:
                    aligned_principles.append(principle_name)
                else:
                    misaligned_principles.append(principle_name)
                    
                # Add to overall alignment
                overall_alignment += score
        
        # Normalize overall alignment
        if alignment_scores:
            overall_alignment /= len(alignment_scores)
        
        return {
            "scores": alignment_scores,
            "overall_alignment": overall_alignment,
            "aligned_principles": aligned_principles,
            "misaligned_principles": misaligned_principles,
            "assessment": "aligned" if overall_alignment >= threshold else "misaligned"
        }
    
    def apply_principles_to_decision(
        self,
        decision_context: Dict[str, Any],
        principles: Optional[List[str]] = None,
        domain_weights: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Apply principles to a decision context.
        
        Args:
            decision_context: Context of the decision
            principles: Optional list of specific principles to apply
            domain_weights: Optional custom domain weights
            
        Returns:
            Updated decision context with principle application results
        """
        # Use default weights if not provided
        domain_weights = domain_weights or self.default_domain_weights
        
        # Make a copy of the context to modify
        updated_context = decision_context.copy()
        
        # If no specific principles provided, select based on context
        if not principles:
            # Get principles for each domain, weighted by domain importance
            selected_principles = []
            for domain, weight in domain_weights.items():
                domain_principles = get_principles_by_domain(domain)
                # Number of principles to select is proportional to domain weight
                num_principles = max(1, int(5 * weight))
                # Select principles (in a real implementation, this would be more sophisticated)
                principle_names = list(domain_principles.keys())
                if principle_names:
                    selected = random.sample(principle_names, min(num_principles, len(principle_names)))
                    selected_principles.extend(selected)
        else:
            selected_principles = principles
            
        # Apply selected principles
        for principle_name in selected_principles:
            updated_context = apply_principle_to_decision(principle_name, updated_context)
            self.principle_usage[principle_name] += 1
            
        # Apply meta-principles to enhance the effects
        principle_set = set(selected_principles)
        enhanced_principles = apply_meta_principles(principle_set)
        
        # Apply any new principles from meta-principle application
        for principle_name in enhanced_principles - principle_set:
            updated_context = apply_principle_to_decision(principle_name, updated_context)
            self.principle_usage[principle_name] += 1
            
        return updated_context
    
    def get_trust_modifiers(
        self,
        agent_id: str,
        agent_data: Dict[str, Any]
    ) -> Dict[str, float]:
        """
        Get principle-based trust modifiers for an agent.
        
        Args:
            agent_id: ID of the agent
            agent_data: Data about the agent
            
        Returns:
            Dictionary of trust modifiers based on principles
        """
        modifiers = {}
        
        # Check for principle alignment
        if 'principle_alignment' in agent_data:
            alignment = agent_data['principle_alignment']
            
            # Add modifiers based on alignment
            if isinstance(alignment, dict) and 'overall_alignment' in alignment:
                # Overall alignment modifier
                modifiers['principle_alignment'] = alignment['overall_alignment'] - 0.5
                
                # Specific principle modifiers for highly aligned principles
                for principle in alignment.get('aligned_principles', []):
                    principle_data = get_principle(principle)
                    if principle_data:
                        domain = principle_data['domain'].split('/')[0]
                        modifier_key = f"aligned_{domain.lower()}"
                        modifiers[modifier_key] = modifiers.get(modifier_key, 0) + 0.1
        
        return modifiers
    
    def get_relevant_principles_for_action(
        self,
        action_type: str,
        context: Dict[str, Any] = None,
        num_principles: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Get principles relevant for a specific action type.
        
        Args:
            action_type: Type of action (e.g., "task_assignment", "agent_registration")
            context: Optional context for the action
            num_principles: Number of principles to return
            
        Returns:
            List of relevant principles with details
        """
        # Define domain weights for different action types
        action_weights = {
            "task_assignment": {"Culture": 0.3, "Tech": 0.5, "Trade": 0.2},
            "agent_registration": {"Culture": 0.5, "Tech": 0.3, "Trade": 0.2},
            "trust_assessment": {"Culture": 0.6, "Tech": 0.2, "Trade": 0.2},
            "message_relay": {"Culture": 0.7, "Tech": 0.2, "Trade": 0.1},
            # Default to balanced weights if action type not recognized
            "default": self.default_domain_weights
        }
        
        # Get weights for this action
        weights = action_weights.get(action_type, action_weights["default"])
        
        # Context description for principle selection
        context_description = f"Action: {action_type}"
        if context:
            # Add relevant context details if available
            if 'description' in context:
                context_description += f", Description: {context['description']}"
            if 'agent_id' in context:
                context_description += f", Agent: {context['agent_id']}"
                
        # Get recommended principles
        principles = []
        for domain, weight in weights.items():
            # Number proportional to domain weight
            count = max(1, int(num_principles * weight))
            domain_principles = get_recommended_principles_for_context(
                context_description, 
                domain=domain,
                num_principles=count
            )
            principles.extend(domain_principles)
            
        # Limit to requested number
        return principles[:num_principles]
    
    def get_usage_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about principle usage.
        
        Returns:
            Dictionary with usage statistics
        """
        total_usage = sum(self.principle_usage.values())
        
        # Calculate domain usage
        domain_usage = {
            "Culture": 0,
            "Tech": 0,
            "Trade": 0
        }
        
        for name, count in self.principle_usage.items():
            principle = get_principle(name)
            if principle:
                domains = principle["domain"].split("/")
                for domain in domains:
                    if domain in domain_usage:
                        domain_usage[domain] += count
        
        # Most and least used principles
        sorted_usage = sorted(
            self.principle_usage.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        most_used = [
            {"name": name, "count": count, "principle": get_principle(name)}
            for name, count in sorted_usage[:5] if count > 0
        ]
        
        least_used = [
            {"name": name, "count": count, "principle": get_principle(name)}
            for name, count in sorted_usage[-5:] if name in ALL_PRINCIPLES
        ]
        
        return {
            "total_usage": total_usage,
            "domain_usage": domain_usage,
            "most_used_principles": most_used,
            "least_used_principles": least_used,
            "unused_principles": [
                name for name, count in self.principle_usage.items() 
                if count == 0 and name in ALL_PRINCIPLES
            ]
        }
    
    def reset_caches(self) -> None:
        """
        Reset all caches.
        """
        self._principle_cache = {}
        self._guidance_cache = {}
        self._relationship_cache = {}
        logger.info("PrincipleEngine caches reset")
        

# Example usage
if __name__ == "__main__":
    engine = PrincipleEngine()
    
    # Create guidance for a task
    guidance = engine.create_guidance_for_task(
        "Design a collaborative decision-making system"
    )
    print(f"Created guidance with {len(guidance['primary_principles'])} primary principles")
    
    # Apply principles to a decision
    decision = {"options": ["A", "B", "C"], "context": "resource allocation"}
    updated = engine.apply_principles_to_decision(decision)
    print(f"Decision updated with {len(updated.get('applied_principles', []))} principles")
