/**
 * CursorBridge API Composable
 * 
 * Provides easy access to CursorBridge APIs from components.
 */

import type { 
  DashboardTemplate, 
  ControlDefinition, 
  ControlPack,
  CouplingRule,
  DerivedMetric,
  ProgrammeProfile,
  SessionRequest,
  SessionOutput
} from '~/types'

export function useBridge() {
  
  // =========================================================================
  // Templates
  // =========================================================================
  
  async function getTemplates(category?: string) {
    const query = category ? `?category=${category}` : ''
    return await $fetch<{ count: number; templates: DashboardTemplate[] }>(
      `/api/bridge/templates${query}`
    )
  }
  
  async function getTemplate(id: string) {
    return await $fetch<DashboardTemplate>(`/api/bridge/templates/${id}`)
  }
  
  // =========================================================================
  // Controls & Packs
  // =========================================================================
  
  async function getControlDefinitions(limit = 100) {
    return await $fetch<{ table: string; count: number; data: ControlDefinition[] }>(
      `/api/bridge/query/control_definitions?limit=${limit}`
    )
  }
  
  async function getControlPacks() {
    return await $fetch<{ table: string; count: number; data: ControlPack[] }>(
      `/api/bridge/query/control_packs`
    )
  }
  
  // =========================================================================
  // Engine Data
  // =========================================================================
  
  async function getCouplingRules() {
    return await $fetch<{ table: string; count: number; data: CouplingRule[] }>(
      `/api/bridge/query/coupling_rules`
    )
  }
  
  async function getDerivedMetrics() {
    return await $fetch<{ table: string; count: number; data: DerivedMetric[] }>(
      `/api/bridge/query/derived_metrics`
    )
  }
  
  // =========================================================================
  // Profiles
  // =========================================================================
  
  async function getProgrammeProfiles() {
    return await $fetch<{ table: string; count: number; data: ProgrammeProfile[] }>(
      `/api/bridge/query/programme_profiles`
    )
  }
  
  // =========================================================================
  // Session Generation
  // =========================================================================
  
  async function generateSession(request: SessionRequest): Promise<SessionOutput> {
    return await $fetch<SessionOutput>('/api/bridge/session', {
      method: 'POST',
      body: request
    })
  }
  
  // =========================================================================
  // Content Queries (generic)
  // =========================================================================
  
  async function queryTable<T = any>(table: string, limit = 100) {
    return await $fetch<{ table: string; count: number; data: T[] }>(
      `/api/bridge/query/${table}?limit=${limit}`
    )
  }
  
  return {
    // Templates
    getTemplates,
    getTemplate,
    
    // Controls
    getControlDefinitions,
    getControlPacks,
    
    // Engine
    getCouplingRules,
    getDerivedMetrics,
    
    // Profiles
    getProgrammeProfiles,
    
    // Sessions
    generateSession,
    
    // Generic
    queryTable,
  }
}






