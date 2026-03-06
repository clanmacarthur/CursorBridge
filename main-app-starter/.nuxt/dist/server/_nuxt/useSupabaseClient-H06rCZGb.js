import { a as useNuxtApp } from "../server.mjs";
const useSupabaseClient = () => {
  return useNuxtApp().$supabase.client;
};
export {
  useSupabaseClient as u
};
//# sourceMappingURL=useSupabaseClient-H06rCZGb.js.map
