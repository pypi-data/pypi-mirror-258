\* Source Pyomo model name=Model *\

min 
objective:
+10 flow(BEV_V2G_storage_BEV_V2G_bus_0_0)

s.t.

c_e_BusBlock_balance(el_bus_0_0)_:
+1 flow(BEV_V2G_v2g_el_bus_0_0)
-1 flow(el_bus_BEV_V2G_storage_0_0)
= -125

c_e_BusBlock_balance(BEV_V2G_bus_0_0)_:
+1 flow(BEV_V2G_storage_BEV_V2G_bus_0_0)
-1 flow(BEV_V2G_bus_BEV_V2G_v2g_0_0)
-1 flow(BEV_V2G_bus_BEV_V2G_consumption_0_0)
= 0

c_e_BusBlock_balance(pkm_bus_0_0)_:
+0 ONE_VAR_CONSTANT
= 0

c_e_ConverterBlock_relation(BEV_V2G_v2g_BEV_V2G_bus_el_bus_0_0)_:
-1 flow(BEV_V2G_v2g_el_bus_0_0)
+1 flow(BEV_V2G_bus_BEV_V2G_v2g_0_0)
= 0

c_e_GenericStorageBlock_balance(BEV_V2G_storage_0_0)_:
+1 flow(BEV_V2G_storage_BEV_V2G_bus_0_0)
-0.8 flow(el_bus_BEV_V2G_storage_0_0)
+1 GenericStorageBlock_storage_content(BEV_V2G_storage_1)
-1 GenericStorageBlock_storage_content(BEV_V2G_storage_0)
= 0

bounds
   1 <= ONE_VAR_CONSTANT <= 1
   0 <= flow(BEV_V2G_storage_BEV_V2G_bus_0_0) <= 200
   0 <= flow(BEV_V2G_v2g_el_bus_0_0) <= 200
   0 <= flow(el_bus_BEV_V2G_storage_0_0) <= 200
   0 <= flow(BEV_V2G_bus_BEV_V2G_v2g_0_0) <= +inf
   0 <= flow(BEV_V2G_bus_BEV_V2G_consumption_0_0) <= 0
   0 <= GenericStorageBlock_storage_content(BEV_V2G_storage_1) <= 200
   0 <= GenericStorageBlock_storage_content(BEV_V2G_storage_0) <= 200
end
