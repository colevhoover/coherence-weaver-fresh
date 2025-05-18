# Technical Context: Coherence Weaver with Participatory Resilience

## Technologies Used

The participatory resilience principles are implemented using the following technologies:

| Technology | Purpose | Principles Alignment |
|------------|---------|---------------------|
| Python 3.9+ | Core implementation language | Supports modular design and community development |
| Type Hints | Code documentation and validation | Enhances interoperability and clarity |
| Asynchronous Functions | Non-blocking operations for distributed decisions | Enables distributed systems architecture |
| Dictionary-based Principle Storage | Flexible principle representation | Facilitates principle adaptation and evolution |
| Weighted Decision Models | Nuanced principle application | Supports proximity to reality and contextual decisions |
| Mermaid Diagrams | Visual relationship documentation | Improves systems translation across domains |

## Development Setup

To work with the participatory resilience implementation:

1. Ensure Python 3.9+ is installed
2. Install from requirements.txt (includes new dependencies)
3. The main participatory resilience module is in `/participatory_resilience.py`
4. Integration points are primarily in the CoherenceWeaverAgent class

## Technical Architecture

The participatory resilience module follows these key architectural patterns:

### 1. Principle Domain Separation

Principles are organized by domain (Core, Cultural, Technical, Trade) to enable:
- Domain-specific application in relevant contexts
- Balanced consideration across domains
- Clear organization for maintenance and extension

```python
# Domain-separated principle dictionaries
CORE_PRINCIPLES = {...}
CULTURAL_PRINCIPLES = {...}
TECHNICAL_PRINCIPLES = {...}
TRADE_PRINCIPLES = {...}

# Combined for convenience
ALL_PRINCIPLES = {
    **CORE_PRINCIPLES,
    **CULTURAL_PRINCIPLES,
    **TECHNICAL_PRINCIPLES,
    **TRADE_PRINCIPLES
}
```

### 2. Function-Based Principle Application

Rather than hard-coding principle effects, the system uses functional application that can be composed and extended:

```python
def apply_principle_to_decision(principle_name, decision_context):
    principle = get_principle(principle_name)
    if not principle:
        return decision_context
    
    updated_context = decision_context.copy()
    
    # Apply domain-specific modifications
    domains = principle["domain"].split("/")
    
    if "Culture" in domains:
        # Cultural domain modifications
        ...
        
    if "Tech" in domains:
        # Technical domain modifications
        ...
        
    if "Trade" in domains:
        # Resource domain modifications
        ...
    
    return updated_context
```

### 3. Meta-Principle Framework

Meta-principles operate on other principles, creating a self-evolving system:

```python
def apply_meta_principles(principles_set):
    enhanced_set = principles_set.copy()
    
    # Find relevant meta-principles based on domain overlap
    relevant_meta = find_relevant_meta_principles(principles_set)
    
    # Apply meta-principles to enhance the set
    for meta_name in relevant_meta:
        enhanced_set = apply_specific_meta_principle(meta_name, enhanced_set)
    
    return enhanced_set
```

### 4. Weighted Guidance Generation

Task-specific guidance uses weighted selection of principles based on domain relevance:

```python
def create_principle_guidance(task_description, domain_weights=None):
    domain_weights = domain_weights or {
        "Culture": 0.4,
        "Tech": 0.4,
        "Trade": 0.2
    }
    
    guidance = {
        "primary_principles": [],
        "supporting_principles": [],
        "meta_principles": []
    }
    
    # Select principles weighted by domain importance
    for domain, weight in domain_weights.items():
        num_principles = max(1, int(5 * weight))
        domain_principles = get_principles_by_domain(domain)
        selected = select_principles_for_context(
            domain_principles, 
            task_description,
            num_principles
        )
        
        # Add to guidance with appropriate weighting
        for name, principle in selected:
            guidance["primary_principles"].append({
                "name": name,
                "description": principle["description"],
                "weight": weight,
                # ...other principle data
            })
    
    # Add related and meta-principles...
    
    return guidance
```

## Integration Points

The participatory resilience principles integrate with the Coherence Weaver agent at several key points:

### 1. CoherenceWeaverAgent Class

The main agent class is enhanced with principle-aware methods:

```python
class CoherenceWeaverAgent(BaseAgent):
    def __init__(self, ...):
        # Initialize principle system
        self.principle_engine = PrincipleEngine()
        
        # Enhanced capabilities list
        capabilities = [
            # Existing capabilities...
            
            # New principle-based capabilities
            AgentCapability(
                name="get_principle_guidance",
                description="Get principle-based guidance for a task",
                parameters={
                    "task_description": {"type": "string", "description": "Description of the task"},
                    "domain_weights": {"type": "object", "description": "Optional weights for different domains"}
                }
            ),
            # Additional principle capabilities...
        ]
        
        super().__init__(name=name, ..., capabilities=capabilities)
```

### 2. Task Orchestration

Task assignment now considers principle guidance:

```python
def assign_task(self, agent_id, description, deadline=None, metadata=None):
    # Get principle guidance for the task
    principle_guidance = self.principle_engine.create_guidance_for_task(description)
    
    # Include principle guidance in task metadata
    if metadata is None:
        metadata = {}
    metadata["principle_guidance"] = principle_guidance
    
    # Continue with existing task assignment process...
    
    # Return enhanced task assignment result
    return {
        "status": "success",
        "message": f"Task assigned to agent {agent_name}",
        "task_id": task_id,
        "conversation_id": conversation_id,
        "principle_guidance": principle_guidance
    }
```

### 3. Agent Registration

Agent registration now includes principle alignment assessment:

```python
def register_agent(self, profile, endpoint, api_key=None):
    # Existing registration logic...
    
    # Assess principle alignment if the agent provides it
    if hasattr(profile, "principle_alignment"):
        alignment_score = self.principle_engine.assess_alignment(
            profile.principle_alignment
        )
        self.registered_agents[agent_id]["principle_alignment"] = alignment_score
    
    # Continue with registration...
```

### 4. Trust Network

Trust calculation now incorporates principle alignment:

```python
def calculate_trust(self, agent_id, interaction_history):
    # Get base trust from interaction history
    base_trust = self.calculate_base_trust(agent_id, interaction_history)
    
    # Apply principle-based trust modifiers
    principle_modifiers = self.principle_engine.get_trust_modifiers(
        agent_id, 
        self.registered_agents.get(agent_id, {})
    )
    
    # Apply modifiers to base trust
    adjusted_trust = apply_trust_modifiers(base_trust, principle_modifiers)
    
    return adjusted_trust
```

## Technical Constraints

1. **Performance Considerations**: 
   - Principle application adds computational overhead
   - Caching strategies are used for frequently accessed principle combinations
   - Heavy principle application is done asynchronously where possible

2. **Backward Compatibility**:
   - All existing APIs maintain their signatures and expected behaviors
   - Principle guidance is optional in all contexts
   - Legacy agents without principle awareness still function in the network

3. **Extensibility Requirements**:
   - New principles can be added without code changes
   - Domain weights are configurable
   - Custom principle application functions can be registered

4. **Graceful Degradation**:
   - System functions even if principle engine fails
   - Default principle sets are provided as fallbacks
   - Errors in principle application do not block critical operations

## Dependencies

New dependencies added for the participatory resilience implementation:

| Dependency | Version | Purpose |
|------------|---------|---------|
| typing-extensions | >= 4.0.0 | Enhanced type annotations |
| aiohttp | >= 3.8.0 | Async HTTP for distributed decisions |
| pydantic | >= 1.9.0 | Data validation for principle structures |
| networkx | >= 2.7.0 | Graph operations for principle relationships |

## Tool Usage

The following development tools support the principle implementation:

1. **Type Checkers**: mypy for validating type correctness
2. **Test Frameworks**: pytest with specific fixtures for principle testing
3. **Documentation**: Sphinx with custom extensions for principle visualization
4. **CI/CD**: GitHub Actions with principle validation steps

## Configuration Management

Principle-related configuration is managed through:

1. A default set of principles in code (participatory_resilience.py)
2. Optional configuration overrides in config/principle_config.json
3. Runtime adjustments via the agent API

Example principle configuration override:
```json
{
  "domain_weights": {
    "default": {
      "Culture": 0.4,
      "Tech": 0.4,
      "Trade": 0.2
    },
    "trust_assessment": {
      "Culture": 0.6,
      "Tech": 0.2,
      "Trade": 0.2
    }
  },
  "principle_priorities": {
    "shared_power_paradigm": 1.2,
    "ethical_design": 1.5
  }
}
