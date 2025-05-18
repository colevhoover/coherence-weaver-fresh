"""
Test script for participatory resilience principles integration.

This script demonstrates the application of participatory resilience principles
to various agent operations and decision contexts.
"""

import sys
import os
import json
from pathlib import Path
import random

# Add the src directory to the path so we can import our modules
sys.path.append(str(Path(__file__).parent.parent / "src"))

from participatory_resilience import (
    get_principle,
    get_principles_by_domain,
    get_related_principles,
    apply_principle_to_decision,
    create_principle_guidance,
    CORE_PRINCIPLES,
    CULTURAL_PRINCIPLES,
    TECHNICAL_PRINCIPLES,
    TRADE_PRINCIPLES,
    ALL_PRINCIPLES,
    META_PRINCIPLES
)
from principle_engine import PrincipleEngine

def print_separator(title):
    """Print a separator with a title."""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80 + "\n")

def test_principle_retrieval():
    """Test basic principle retrieval functions."""
    print_separator("Testing Principle Retrieval")
    
    # Get a principle by name
    principle_name = "shared_power_paradigm"
    principle = get_principle(principle_name)
    
    print(f"Retrieved principle '{principle_name}':")
    print(f"  Description: {principle['description']}")
    print(f"  Effect: {principle['effect']}")
    print(f"  Domain: {principle['domain']}")
    
    # Get principles by domain
    domain = "Tech"
    tech_principles = get_principles_by_domain(domain)
    
    print(f"\nFound {len(tech_principles)} principles in the {domain} domain:")
    for name, principle in list(tech_principles.items())[:3]:  # Show first 3 for brevity
        print(f"  - {name}: {principle['description']}")
    
    if len(tech_principles) > 3:
        print(f"  - ... and {len(tech_principles) - 3} more")
    
    # Get related principles
    principle_name = "distributed_systems_architecture"
    related = get_related_principles(principle_name)
    
    print(f"\nFound {len(related)} principles related to '{principle_name}':")
    for name, principle in list(related.items())[:3]:  # Show first 3 for brevity
        print(f"  - {name}: {principle['description']} ({principle['domain']})")
    
    if len(related) > 3:
        print(f"  - ... and {len(related) - 3} more")

def test_principle_application():
    """Test applying principles to decisions."""
    print_separator("Testing Principle Application")
    
    # Create a simple decision context
    decision = {
        "task": "resource_allocation",
        "options": ["centralized", "distributed", "hybrid"],
        "constraints": ["time_sensitive", "security_critical"]
    }
    
    print("Original decision context:")
    print(json.dumps(decision, indent=2))
    
    # Apply a principle
    principle_name = "distributed_systems_architecture"
    updated = apply_principle_to_decision(principle_name, decision)
    
    print(f"\nAfter applying '{principle_name}':")
    print(json.dumps(updated, indent=2))
    
    # Apply a cultural principle
    principle_name = "community_wisdom"
    updated = apply_principle_to_decision(principle_name, updated)
    
    print(f"\nAfter also applying '{principle_name}':")
    print(json.dumps(updated, indent=2))

def test_principle_guidance():
    """Test creating principle guidance for tasks."""
    print_separator("Testing Principle Guidance")
    
    # Create guidance for a task
    task_description = "Design a collaborative decision-making system for autonomous agents"
    guidance = create_principle_guidance(task_description)
    
    print(f"Generated guidance for: '{task_description}'")
    print(f"\nPrimary principles ({len(guidance['primary_principles'])}):")
    for principle in guidance['primary_principles']:
        print(f"  - {principle['name']} ({principle['domain']}): {principle['description']}")
    
    print(f"\nSupporting principles ({len(guidance['supporting_principles'])}):")
    for principle in guidance['supporting_principles']:
        print(f"  - {principle['name']} ({principle['domain']}): {principle['description']}")
    
    print(f"\nMeta principles ({len(guidance['meta_principles'])}):")
    for principle in guidance['meta_principles']:
        print(f"  - {principle['name']} ({principle['domain']}): {principle['description']}")

def test_principle_engine():
    """Test the PrincipleEngine class."""
    print_separator("Testing PrincipleEngine")
    
    # Create a principle engine with the config file
    config_path = Path(__file__).parent.parent / "config" / "principle_config.json"
    engine = PrincipleEngine(config_path=str(config_path))
    
    print("PrincipleEngine initialized with configuration.")
    
    # Create guidance for a task
    task_description = "Orchestrate a multi-agent task involving data analysis and visualization"
    guidance = engine.create_guidance_for_task(task_description)
    
    print(f"Generated guidance for task: '{task_description}'")
    print(f"  - Primary principles: {len(guidance['primary_principles'])}")
    print(f"  - Supporting principles: {len(guidance['supporting_principles'])}")
    print(f"  - Meta principles: {len(guidance['meta_principles'])}")
    
    # Apply principles to a decision
    decision = {
        "task_type": "data_processing",
        "agent_candidates": ["agent1", "agent2", "agent3"],
        "priority": "high",
        "requires_coordination": True
    }
    
    updated = engine.apply_principles_to_decision(decision)
    
    print("\nDecision after applying principles:")
    print(json.dumps(updated, indent=2))
    
    # Assess principle alignment
    agent_principles = {
        "shared_power_paradigm": 0.8,
        "ethical_design": 0.9,
        "distributed_systems_architecture": 0.7,
        "open_source_philosophy": 0.6,
        "unknown_principle": 0.5  # This one doesn't exist in our system
    }
    
    alignment = engine.assess_alignment(agent_principles)
    
    print("\nPrinciple alignment assessment:")
    print(f"  - Overall alignment: {alignment['overall_alignment']:.2f}")
    print(f"  - Assessment: {alignment['assessment']}")
    print(f"  - Aligned principles: {', '.join(alignment['aligned_principles'])}")
    print(f"  - Misaligned principles: {', '.join(alignment['misaligned_principles'])}")

def test_practical_scenario():
    """Test a practical scenario using the principle system."""
    print_separator("Testing Practical Scenario")
    
    # Initialize the engine
    config_path = Path(__file__).parent.parent / "config" / "principle_config.json"
    engine = PrincipleEngine(config_path=str(config_path))
    
    print("Scenario: Task Assignment in a Distributed Agent Network")
    print("\nStep 1: Get principle guidance for the task type")
    
    # Get principles for task assignment
    task_principles = engine.get_relevant_principles_for_action(
        "task_assignment",
        context={"description": "Process and analyze large dataset"},
        num_principles=3
    )
    
    print("Relevant principles for task assignment:")
    for principle in task_principles:
        print(f"  - {principle['name']}: {principle['description']}")
    
    print("\nStep 2: Evaluate candidate agents based on principle alignment")
    
    # Simulated agent data with principle alignment scores
    agents = {
        "agent1": {
            "name": "Data Analysis Agent",
            "capabilities": ["data_processing", "statistical_analysis"],
            "principle_alignment": {
                "distributed_systems_architecture": 0.9,
                "data_driven_decision_making": 0.8,
                "community_wisdom": 0.6
            },
            "current_load": 0.3
        },
        "agent2": {
            "name": "Visualization Agent",
            "capabilities": ["data_visualization", "interactive_dashboards"],
            "principle_alignment": {
                "human_centered_technology": 0.9,
                "ethical_design": 0.7,
                "inclusive_design_paradigm": 0.8
            },
            "current_load": 0.5
        },
        "agent3": {
            "name": "Coordination Agent",
            "capabilities": ["task_management", "agent_coordination"],
            "principle_alignment": {
                "shared_power_paradigm": 0.9,
                "catalytic_facilitation": 0.8,
                "systems_translation": 0.8
            },
            "current_load": 0.7
        }
    }
    
    # Evaluate agents based on principle alignment and other factors
    evaluations = {}
    for agent_id, agent_data in agents.items():
        # Calculate base score (simplified for demonstration)
        base_score = (1 - agent_data["current_load"]) * 0.5
        
        # Calculate principle alignment score
        alignment_score = 0
        alignment_count = 0
        
        for principle in task_principles:
            if principle["name"] in agent_data.get("principle_alignment", {}):
                alignment_score += agent_data["principle_alignment"][principle["name"]]
                alignment_count += 1
        
        if alignment_count > 0:
            alignment_score /= alignment_count
            
        # Get trust modifiers based on principle alignment
        trust_modifiers = engine.get_trust_modifiers(agent_id, agent_data)
        trust_score = sum(trust_modifiers.values()) if trust_modifiers else 0
        
        # Calculate final score
        final_score = base_score + (alignment_score * 0.3) + (trust_score * 0.2)
        
        evaluations[agent_id] = {
            "agent_name": agent_data["name"],
            "base_score": base_score,
            "alignment_score": alignment_score,
            "trust_score": trust_score,
            "final_score": final_score
        }
    
    # Print evaluations
    print("Agent evaluations based on principle alignment:")
    for agent_id, evaluation in evaluations.items():
        print(f"  - {evaluation['agent_name']} (ID: {agent_id}):")
        print(f"    - Final score: {evaluation['final_score']:.2f}")
        print(f"    - Base score: {evaluation['base_score']:.2f}")
        print(f"    - Alignment score: {evaluation['alignment_score']:.2f}")
        print(f"    - Trust score: {evaluation['trust_score']:.2f}")
    
    # Select the best agent
    best_agent_id = max(evaluations, key=lambda a: evaluations[a]["final_score"])
    best_agent = agents[best_agent_id]
    
    print(f"\nSelected agent: {best_agent['name']} (ID: {best_agent_id})")
    
    print("\nStep 3: Create principle-guided task assignment")
    
    # Create task with principle guidance
    task = {
        "id": f"task_{random.randint(1000, 9999)}",
        "description": "Process and analyze large dataset",
        "assigned_agent_id": best_agent_id,
        "deadline": "2025-05-25T12:00:00Z",
        "priority": "high",
        "principle_guidance": engine.create_guidance_for_task(
            "Process and analyze large dataset",
            context={"agent_id": best_agent_id}
        )
    }
    
    print("Task created with principle guidance:")
    print(f"  - Task ID: {task['id']}")
    print(f"  - Description: {task['description']}")
    print(f"  - Assigned to: {best_agent['name']} (ID: {best_agent_id})")
    print(f"  - Guidance includes {len(task['principle_guidance']['primary_principles'])} primary principles")
    
    print("\nStep 4: Apply principles to final decision context")
    
    # Create decision context for assignment
    decision_context = {
        "task_id": task["id"],
        "agent_id": best_agent_id,
        "deadline": task["deadline"],
        "priority": task["priority"],
        "resources_allocated": {},
        "coordination_requirements": []
    }
    
    # Apply principles to decision
    final_context = engine.apply_principles_to_decision(decision_context)
    
    # Print the differences/enhancements made by principle application
    print("Principle application enhanced the task assignment with:")
    
    if "applied_principles" in final_context:
        print(f"  - Applied {len(final_context['applied_principles'])} principles:")
        for p in final_context["applied_principles"]:
            print(f"    - {p['name']}: {p['effect']}")
    
    for key, value in final_context.items():
        if key not in decision_context or decision_context[key] != value:
            if key != "applied_principles":
                print(f"  - Enhanced {key}: {value}")

if __name__ == "__main__":
    # Ensure we have a config directory
    config_dir = Path(__file__).parent.parent / "config"
    if not config_dir.exists():
        print(f"Warning: Config directory {config_dir} not found")
    
    try:
        test_principle_retrieval()
        test_principle_application()
        test_principle_guidance()
        test_principle_engine()
        test_practical_scenario()
        
        print_separator("All Tests Completed Successfully")
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()
