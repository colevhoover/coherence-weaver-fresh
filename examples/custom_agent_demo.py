"""
Custom Agent Demo

This script demonstrates how to create and use a custom agent that extends BaseAgent.
"""

import sys
import os
import uuid
from pathlib import Path

# Add the parent directory to the Python path so we can import from src
sys.path.append(str(Path(__file__).parent.parent))

from src.agents.base_agent import BaseAgent
from src.models.agent_models import AgentCapability, MessageRole


class ResearchAgent(BaseAgent):
    """
    A specialized agent that can perform research tasks.
    
    This demonstrates how to extend BaseAgent to create custom agent types
    with specialized capabilities.
    """
    
    def __init__(self, name="Research Agent", description="An agent that can perform research tasks", **kwargs):
        # Define agent capabilities
        capabilities = [
            AgentCapability(
                name="search_topic",
                description="Search for information on a topic",
                parameters={
                    "topic": {"type": "string", "description": "The topic to research"},
                    "depth": {"type": "integer", "description": "How deeply to research the topic"}
                }
            ),
            AgentCapability(
                name="summarize",
                description="Summarize collected information",
                parameters={
                    "max_length": {"type": "integer", "description": "Maximum length of the summary"}
                }
            ),
            AgentCapability(
                name="cite_sources",
                description="Cite sources for collected information",
                parameters={
                    "format": {"type": "string", "description": "Citation format (APA, MLA, etc.)"}
                }
            )
        ]
        
        # Initialize the base agent
        super().__init__(
            name=name,
            description=description,
            capabilities=capabilities,
            **kwargs
        )
        
        # Initialize research-specific attributes
        self.research_topics = {}
        self.current_topic = None
    
    def search_topic(self, topic, depth=3):
        """
        Simulate searching for information on a topic.
        
        Args:
            topic: Topic to research
            depth: How deeply to research the topic
            
        Returns:
            dict: Research results
        """
        # In a real implementation, this would perform actual research
        # For this demo, we'll simulate it
        topic_id = str(uuid.uuid4())
        
        # Create a conversation for this research topic
        conversation_id = self.create_conversation(
            system_prompt=f"Research on topic: {topic} with depth {depth}"
        )
        
        # Add a message to the conversation
        self.add_message(
            conversation_id=conversation_id,
            role=MessageRole.SYSTEM,
            content=f"Beginning research on topic: {topic} with depth {depth}"
        )
        
        # Store the topic information
        self.research_topics[topic_id] = {
            "topic": topic,
            "depth": depth,
            "conversation_id": conversation_id,
            "status": "in_progress",
            "findings": f"Simulated research findings for {topic} at depth {depth}",
            "sources": [
                f"Source 1 for {topic}",
                f"Source 2 for {topic}",
                f"Source 3 for {topic}"
            ]
        }
        
        self.current_topic = topic_id
        
        return {
            "topic_id": topic_id,
            "message": f"Research started on topic: {topic}",
            "conversation_id": conversation_id
        }
    
    def summarize(self, topic_id=None, max_length=500):
        """
        Summarize the research findings for a topic.
        
        Args:
            topic_id: ID of the topic to summarize (uses current topic if None)
            max_length: Maximum length of the summary
            
        Returns:
            dict: Summary information
        """
        topic_id = topic_id or self.current_topic
        
        if not topic_id or topic_id not in self.research_topics:
            return {
                "error": "Topic not found"
            }
        
        topic_info = self.research_topics[topic_id]
        
        # In a real implementation, this would generate an actual summary
        # using generative AI based on the collected information
        summary = f"Summary of research on {topic_info['topic']} (limited to {max_length} chars)"
        
        # Add the summary to the conversation
        self.add_message(
            conversation_id=topic_info["conversation_id"],
            role=MessageRole.ASSISTANT,
            content=summary,
            name=self.profile.name,
            agent_id=self.agent_id
        )
        
        return {
            "topic": topic_info["topic"],
            "summary": summary,
            "length": len(summary)
        }
    
    def cite_sources(self, topic_id=None, format="APA"):
        """
        Cite sources for the research findings.
        
        Args:
            topic_id: ID of the topic to cite sources for (uses current topic if None)
            format: Citation format (APA, MLA, etc.)
            
        Returns:
            dict: Citation information
        """
        topic_id = topic_id or self.current_topic
        
        if not topic_id or topic_id not in self.research_topics:
            return {
                "error": "Topic not found"
            }
        
        topic_info = self.research_topics[topic_id]
        
        # In a real implementation, this would format actual citations
        # For this demo, we'll simulate it
        citations = [
            f"{format} citation for source 1 on {topic_info['topic']}",
            f"{format} citation for source 2 on {topic_info['topic']}",
            f"{format} citation for source 3 on {topic_info['topic']}"
        ]
        
        return {
            "topic": topic_info["topic"],
            "format": format,
            "citations": citations
        }


def main():
    """
    Main function to demonstrate the ResearchAgent.
    """
    print("=== Research Agent Demo ===\n")
    
    # Create a ResearchAgent instance
    agent = ResearchAgent(
        name="ResearchGPT",
        description="An agent that specializes in research tasks",
        temperature=0.3,  # Lower temperature for more factual responses
    )
    
    print(f"Created agent: {agent.profile.name}")
    print(f"Agent ID: {agent.agent_id}")
    print(f"Agent capabilities:")
    for capability in agent.capabilities:
        print(f"  - {capability.name}: {capability.description}")
    
    print("\n--- Starting Research ---")
    
    # Start research on a topic
    topic = "Agent-to-Agent Communication Protocols"
    result = agent.search_topic(topic, depth=4)
    print(f"Research started: {result['message']}")
    print(f"Topic ID: {result['topic_id']}")
    
    # Generate a summary
    summary_result = agent.summarize(max_length=300)
    print(f"\nSummary of research on '{summary_result['topic']}':")
    print(f"{summary_result['summary']}")
    
    # Cite sources
    citation_result = agent.cite_sources(format="MLA")
    print(f"\nCitations for research on '{citation_result['topic']}' in {citation_result['format']} format:")
    for citation in citation_result['citations']:
        print(f"  {citation}")
    
    print("\n=== Demo completed ===")


if __name__ == "__main__":
    main()
