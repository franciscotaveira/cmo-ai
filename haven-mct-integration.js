/**
 * HAVEN RECEPTIONIST — MCT Core Integration
 * Integra Haven com o MCT Orchestrator
 */

import express from 'express';
import cors from 'cors';
import { createClient } from 'redis';
import orchestrator from '../../core/orchestrator/index.js';
import { createSkills, getToolDefinitions } from '../../core/skills/index.js';
import knowledgeBase from '../../core/knowledge/index.js';
import { evolutionApi } from '../../core/tools/evolution.tool.js';
import { supabase } from '../../core/tools/supabase.tool.js';

// Webhook routes (simplified)
import webhookRoutes from './routes/webhook.js';

const app = express();
const PORT = process.env.PORT || 3003;

// Middleware
app.use(cors());
app.use(express.json());

async function bootstrap() {
  console.log('[HAVEN] Starting MCT Core Integration...');
  
  // Redis
  const redis = createClient({ url: process.env.REDIS_URL || 'redis://localhost:6379' });
  await redis.connect();
  console.log('📦 Connected to Redis');

  // Criar skills com dependências
  const skills = createSkills({
    evolutionApi: evolutionApi,
    supabase: supabase
  });

  // Registrar skills no orquestrador
  orchestrator.registerSkills(skills);
  console.log('🛠️ Skills registered:', Object.keys(skills).join(', '));

  // Registrar agente Haven
  orchestrator.registerAgent('haven', {
    name: 'Haven Receptionist',
    type: 'receptionist',
    tenant: 'haven-escovaria',
    config: {
      personality: { tone: 'professional', traits: ['helpful', 'friendly'] },
      business: { name: 'Haven Esmalteria & Escovaria', location: 'Chapecó, SC' }
    }
  });
  console.log('🤖 Haven agent registered');

  // Carregar knowledge base
  await knowledgeBase.load('haven-receptionist');
  console.log('📚 Knowledge base loaded');

  // Rotas
  app.use('/webhook', webhookRoutes);

  // Health check
  app.get('/health', (req, res) => {
    res.json({ 
      status: 'ok', 
      agent: 'Haven Receptionist',
      mct: true,
      skills: Object.keys(skills),
      orchestrator: orchestrator.getStatus()
    });
  });

  // Test endpoint
  app.post('/test', async (req, res) => {
    const { message, userId } = req.body;
    
    try {
      const result = await orchestrator.processTask({
        agentId: 'haven',
        userId: userId || 'test-user',
        message,
        context: {}
      });
      res.json(result);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  });

  // Start server
  app.listen(PORT, () => {
    console.log(`🚀 Haven Receptionist running on port ${PORT}`);
    console.log(`📊 MCT Core Integration active`);
    console.log(`🧠 Orchestrator status:`, orchestrator.getStatus());
  });
}

bootstrap().catch(console.error);
