// 🍃 MongoDB Initialization Script
// Ultra Advanced AI Agent System

db = db.getSiblingDB('ai_agent_system');

// Create collections
db.createCollection('knowledge_base');
db.createCollection('vector_embeddings');
db.createCollection('agent_memory');
db.createCollection('workflow_definitions');
db.createCollection('automation_rules');

// Create indexes
db.knowledge_base.createIndex({ "title": "text", "content": "text" });
db.knowledge_base.createIndex({ "category": 1 });
db.knowledge_base.createIndex({ "created_at": -1 });

db.vector_embeddings.createIndex({ "source_id": 1 });
db.vector_embeddings.createIndex({ "source_type": 1 });
db.vector_embeddings.createIndex({ "created_at": -1 });

db.agent_memory.createIndex({ "agent_id": 1 });
db.agent_memory.createIndex({ "memory_type": 1 });
db.agent_memory.createIndex({ "created_at": -1 });

db.workflow_definitions.createIndex({ "name": 1 });
db.workflow_definitions.createIndex({ "status": 1 });
db.workflow_definitions.createIndex({ "created_at": -1 });

db.automation_rules.createIndex({ "trigger_type": 1 });
db.automation_rules.createIndex({ "is_active": 1 });
db.automation_rules.createIndex({ "created_at": -1 });

// Insert sample data
db.knowledge_base.insertOne({
    title: "System Initialization",
    content: "AI Agent System has been successfully initialized with multi-provider support.",
    category: "system",
    tags: ["initialization", "system"],
    metadata: {
        providers: ["nvidia", "sambanova", "cerebras"],
        capabilities: ["chat", "code-generation", "reasoning", "analytics"]
    },
    created_at: new Date(),
    updated_at: new Date()
});

print("✅ MongoDB initialized successfully!");
print("📊 Collections created: knowledge_base, vector_embeddings, agent_memory, workflow_definitions, automation_rules");