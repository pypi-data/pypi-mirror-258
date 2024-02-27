\* Source Pyomo model name=Model *\

min 
objective:
+1374.3355059550622 ONE_VAR_CONSTANT
+11.388767263673406 InvestmentFlowBlock_invest(el_bus_BEV_V2G_storage_0)
+7.992453207841759 InvestmentFlowBlock_invest(el_bus_BEV_V2G_storage_1)
+1.2231343625058069 InvestmentFlowBlock_invest(wind_el_bus_0)
+1.0033961948005203 InvestmentFlowBlock_invest(wind_el_bus_1)
+3 flow(el_bus_BEV_V2G_storage_0_0)
+3 flow(el_bus_BEV_V2G_storage_0_1)
+3 flow(el_bus_BEV_V2G_storage_0_2)
+2.4610448996254655 flow(el_bus_BEV_V2G_storage_1_3)
+2.4610448996254655 flow(el_bus_BEV_V2G_storage_1_4)
+2.4610448996254655 flow(el_bus_BEV_V2G_storage_1_5)

s.t.

c_e_BusBlock_balance(pkm_bus_0_0)_:
+1 flow(BEV_V2G_2com_pkm_bus_0_0)
= 0

c_e_BusBlock_balance(pkm_bus_0_1)_:
+1 flow(BEV_V2G_2com_pkm_bus_0_1)
= 200

c_e_BusBlock_balance(pkm_bus_0_2)_:
+1 flow(BEV_V2G_2com_pkm_bus_0_2)
= 0

c_e_BusBlock_balance(pkm_bus_1_3)_:
+1 flow(BEV_V2G_2com_pkm_bus_1_3)
= 0

c_e_BusBlock_balance(pkm_bus_1_4)_:
+1 flow(BEV_V2G_2com_pkm_bus_1_4)
= 200

c_e_BusBlock_balance(pkm_bus_1_5)_:
+1 flow(BEV_V2G_2com_pkm_bus_1_5)
= 0

c_e_BusBlock_balance(BEV_V2G_bus_0_0)_:
+1 flow(BEV_V2G_storage_BEV_V2G_bus_0_0)
-1 flow(BEV_V2G_bus_BEV_V2G_v2g_0_0)
-1 flow(BEV_V2G_bus_BEV_V2G_2com_0_0)
= 0

c_e_BusBlock_balance(BEV_V2G_bus_0_1)_:
+1 flow(BEV_V2G_storage_BEV_V2G_bus_0_1)
-1 flow(BEV_V2G_bus_BEV_V2G_v2g_0_1)
-1 flow(BEV_V2G_bus_BEV_V2G_2com_0_1)
= 0

c_e_BusBlock_balance(BEV_V2G_bus_0_2)_:
+1 flow(BEV_V2G_storage_BEV_V2G_bus_0_2)
-1 flow(BEV_V2G_bus_BEV_V2G_v2g_0_2)
-1 flow(BEV_V2G_bus_BEV_V2G_2com_0_2)
= 0

c_e_BusBlock_balance(BEV_V2G_bus_1_3)_:
+1 flow(BEV_V2G_storage_BEV_V2G_bus_1_3)
-1 flow(BEV_V2G_bus_BEV_V2G_v2g_1_3)
-1 flow(BEV_V2G_bus_BEV_V2G_2com_1_3)
= 0

c_e_BusBlock_balance(BEV_V2G_bus_1_4)_:
+1 flow(BEV_V2G_storage_BEV_V2G_bus_1_4)
-1 flow(BEV_V2G_bus_BEV_V2G_v2g_1_4)
-1 flow(BEV_V2G_bus_BEV_V2G_2com_1_4)
= 0

c_e_BusBlock_balance(BEV_V2G_bus_1_5)_:
+1 flow(BEV_V2G_storage_BEV_V2G_bus_1_5)
-1 flow(BEV_V2G_bus_BEV_V2G_v2g_1_5)
-1 flow(BEV_V2G_bus_BEV_V2G_2com_1_5)
= 0

c_e_BusBlock_balance(el_bus_0_0)_:
-1 flow(el_bus_BEV_V2G_storage_0_0)
+1 flow(wind_el_bus_0_0)
+1 flow(BEV_V2G_v2g_el_bus_0_0)
= 100

c_e_BusBlock_balance(el_bus_0_1)_:
-1 flow(el_bus_BEV_V2G_storage_0_1)
+1 flow(wind_el_bus_0_1)
+1 flow(BEV_V2G_v2g_el_bus_0_1)
= 100

c_e_BusBlock_balance(el_bus_0_2)_:
-1 flow(el_bus_BEV_V2G_storage_0_2)
+1 flow(wind_el_bus_0_2)
+1 flow(BEV_V2G_v2g_el_bus_0_2)
= 100

c_e_BusBlock_balance(el_bus_1_3)_:
-1 flow(el_bus_BEV_V2G_storage_1_3)
+1 flow(wind_el_bus_1_3)
+1 flow(BEV_V2G_v2g_el_bus_1_3)
= 100

c_e_BusBlock_balance(el_bus_1_4)_:
-1 flow(el_bus_BEV_V2G_storage_1_4)
+1 flow(wind_el_bus_1_4)
+1 flow(BEV_V2G_v2g_el_bus_1_4)
= 100

c_e_BusBlock_balance(el_bus_1_5)_:
-1 flow(el_bus_BEV_V2G_storage_1_5)
+1 flow(wind_el_bus_1_5)
+1 flow(BEV_V2G_v2g_el_bus_1_5)
= 100

c_e_ConverterBlock_relation(BEV_V2G_2com_BEV_V2G_bus_pkm_bus_0_0)_:
-0.7 flow(BEV_V2G_2com_pkm_bus_0_0)
+1 flow(BEV_V2G_bus_BEV_V2G_2com_0_0)
= 0

c_e_ConverterBlock_relation(BEV_V2G_v2g_BEV_V2G_bus_el_bus_0_0)_:
+1 flow(BEV_V2G_bus_BEV_V2G_v2g_0_0)
-1 flow(BEV_V2G_v2g_el_bus_0_0)
= 0

c_e_ConverterBlock_relation(BEV_V2G_2com_BEV_V2G_bus_pkm_bus_0_1)_:
-0.7 flow(BEV_V2G_2com_pkm_bus_0_1)
+1 flow(BEV_V2G_bus_BEV_V2G_2com_0_1)
= 0

c_e_ConverterBlock_relation(BEV_V2G_v2g_BEV_V2G_bus_el_bus_0_1)_:
+1 flow(BEV_V2G_bus_BEV_V2G_v2g_0_1)
-1 flow(BEV_V2G_v2g_el_bus_0_1)
= 0

c_e_ConverterBlock_relation(BEV_V2G_2com_BEV_V2G_bus_pkm_bus_0_2)_:
-0.7 flow(BEV_V2G_2com_pkm_bus_0_2)
+1 flow(BEV_V2G_bus_BEV_V2G_2com_0_2)
= 0

c_e_ConverterBlock_relation(BEV_V2G_v2g_BEV_V2G_bus_el_bus_0_2)_:
+1 flow(BEV_V2G_bus_BEV_V2G_v2g_0_2)
-1 flow(BEV_V2G_v2g_el_bus_0_2)
= 0

c_e_ConverterBlock_relation(BEV_V2G_2com_BEV_V2G_bus_pkm_bus_1_3)_:
-0.7 flow(BEV_V2G_2com_pkm_bus_1_3)
+1 flow(BEV_V2G_bus_BEV_V2G_2com_1_3)
= 0

c_e_ConverterBlock_relation(BEV_V2G_v2g_BEV_V2G_bus_el_bus_1_3)_:
+1 flow(BEV_V2G_bus_BEV_V2G_v2g_1_3)
-1 flow(BEV_V2G_v2g_el_bus_1_3)
= 0

c_e_ConverterBlock_relation(BEV_V2G_2com_BEV_V2G_bus_pkm_bus_1_4)_:
-0.7 flow(BEV_V2G_2com_pkm_bus_1_4)
+1 flow(BEV_V2G_bus_BEV_V2G_2com_1_4)
= 0

c_e_ConverterBlock_relation(BEV_V2G_v2g_BEV_V2G_bus_el_bus_1_4)_:
+1 flow(BEV_V2G_bus_BEV_V2G_v2g_1_4)
-1 flow(BEV_V2G_v2g_el_bus_1_4)
= 0

c_e_ConverterBlock_relation(BEV_V2G_2com_BEV_V2G_bus_pkm_bus_1_5)_:
-0.7 flow(BEV_V2G_2com_pkm_bus_1_5)
+1 flow(BEV_V2G_bus_BEV_V2G_2com_1_5)
= 0

c_e_ConverterBlock_relation(BEV_V2G_v2g_BEV_V2G_bus_el_bus_1_5)_:
+1 flow(BEV_V2G_bus_BEV_V2G_v2g_1_5)
-1 flow(BEV_V2G_v2g_el_bus_1_5)
= 0

c_e_InvestmentFlowBlock_total_rule(wind_el_bus_0)_:
-1 InvestmentFlowBlock_invest(wind_el_bus_0)
+1 InvestmentFlowBlock_total(wind_el_bus_0)
= 200

c_e_InvestmentFlowBlock_total_rule(wind_el_bus_1)_:
-1 InvestmentFlowBlock_invest(wind_el_bus_1)
-1 InvestmentFlowBlock_total(wind_el_bus_0)
+1 InvestmentFlowBlock_total(wind_el_bus_1)
+1 InvestmentFlowBlock_old(wind_el_bus_1)
= 0

c_e_InvestmentFlowBlock_total_rule(BEV_V2G_v2g_el_bus_0)_:
+1 InvestmentFlowBlock_total(BEV_V2G_v2g_el_bus_0)
-1 InvestmentFlowBlock_invest(BEV_V2G_v2g_el_bus_0)
= 150

c_e_InvestmentFlowBlock_total_rule(BEV_V2G_v2g_el_bus_1)_:
-1 InvestmentFlowBlock_total(BEV_V2G_v2g_el_bus_0)
+1 InvestmentFlowBlock_total(BEV_V2G_v2g_el_bus_1)
-1 InvestmentFlowBlock_invest(BEV_V2G_v2g_el_bus_1)
+1 InvestmentFlowBlock_old(BEV_V2G_v2g_el_bus_1)
= 0

c_e_InvestmentFlowBlock_total_rule(BEV_V2G_2com_pkm_bus_0)_:
+1 InvestmentFlowBlock_total(BEV_V2G_2com_pkm_bus_0)
-1 InvestmentFlowBlock_invest(BEV_V2G_2com_pkm_bus_0)
= 150

c_e_InvestmentFlowBlock_total_rule(BEV_V2G_2com_pkm_bus_1)_:
-1 InvestmentFlowBlock_total(BEV_V2G_2com_pkm_bus_0)
+1 InvestmentFlowBlock_total(BEV_V2G_2com_pkm_bus_1)
-1 InvestmentFlowBlock_invest(BEV_V2G_2com_pkm_bus_1)
+1 InvestmentFlowBlock_old(BEV_V2G_2com_pkm_bus_1)
= 0

c_e_InvestmentFlowBlock_total_rule(BEV_V2G_storage_BEV_V2G_bus_0)_:
+1 InvestmentFlowBlock_total(BEV_V2G_storage_BEV_V2G_bus_0)
-1 InvestmentFlowBlock_invest(BEV_V2G_storage_BEV_V2G_bus_0)
= 150

c_e_InvestmentFlowBlock_total_rule(BEV_V2G_storage_BEV_V2G_bus_1)_:
-1 InvestmentFlowBlock_total(BEV_V2G_storage_BEV_V2G_bus_0)
+1 InvestmentFlowBlock_total(BEV_V2G_storage_BEV_V2G_bus_1)
-1 InvestmentFlowBlock_invest(BEV_V2G_storage_BEV_V2G_bus_1)
+1 InvestmentFlowBlock_old(BEV_V2G_storage_BEV_V2G_bus_1)
= 0

c_e_InvestmentFlowBlock_total_rule(el_bus_BEV_V2G_storage_0)_:
-1 InvestmentFlowBlock_invest(el_bus_BEV_V2G_storage_0)
+1 InvestmentFlowBlock_total(el_bus_BEV_V2G_storage_0)
= 150

c_e_InvestmentFlowBlock_total_rule(el_bus_BEV_V2G_storage_1)_:
-1 InvestmentFlowBlock_invest(el_bus_BEV_V2G_storage_1)
-1 InvestmentFlowBlock_total(el_bus_BEV_V2G_storage_0)
+1 InvestmentFlowBlock_total(el_bus_BEV_V2G_storage_1)
+1 InvestmentFlowBlock_old(el_bus_BEV_V2G_storage_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(wind_el_bus_0)_:
+1 InvestmentFlowBlock_old_end(wind_el_bus_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(wind_el_bus_1)_:
+1 InvestmentFlowBlock_old_end(wind_el_bus_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(BEV_V2G_v2g_el_bus_0)_:
+1 InvestmentFlowBlock_old_end(BEV_V2G_v2g_el_bus_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(BEV_V2G_v2g_el_bus_1)_:
-1 InvestmentFlowBlock_invest(BEV_V2G_v2g_el_bus_0)
+1 InvestmentFlowBlock_old_end(BEV_V2G_v2g_el_bus_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(BEV_V2G_2com_pkm_bus_0)_:
+1 InvestmentFlowBlock_old_end(BEV_V2G_2com_pkm_bus_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(BEV_V2G_2com_pkm_bus_1)_:
-1 InvestmentFlowBlock_invest(BEV_V2G_2com_pkm_bus_0)
+1 InvestmentFlowBlock_old_end(BEV_V2G_2com_pkm_bus_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(BEV_V2G_storage_BEV_V2G_bus_0)_:
+1 InvestmentFlowBlock_old_end(BEV_V2G_storage_BEV_V2G_bus_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(BEV_V2G_storage_BEV_V2G_bus_1)_:
-1 InvestmentFlowBlock_invest(BEV_V2G_storage_BEV_V2G_bus_0)
+1 InvestmentFlowBlock_old_end(BEV_V2G_storage_BEV_V2G_bus_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(el_bus_BEV_V2G_storage_0)_:
+1 InvestmentFlowBlock_old_end(el_bus_BEV_V2G_storage_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(el_bus_BEV_V2G_storage_1)_:
-1 InvestmentFlowBlock_invest(el_bus_BEV_V2G_storage_0)
+1 InvestmentFlowBlock_old_end(el_bus_BEV_V2G_storage_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(wind_el_bus_0)_:
+1 InvestmentFlowBlock_old_exo(wind_el_bus_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(wind_el_bus_1)_:
+1 InvestmentFlowBlock_old_exo(wind_el_bus_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(BEV_V2G_v2g_el_bus_0)_:
+1 InvestmentFlowBlock_old_exo(BEV_V2G_v2g_el_bus_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(BEV_V2G_v2g_el_bus_1)_:
+1 InvestmentFlowBlock_old_exo(BEV_V2G_v2g_el_bus_1)
= 150

c_e_InvestmentFlowBlock_old_rule_exo(BEV_V2G_2com_pkm_bus_0)_:
+1 InvestmentFlowBlock_old_exo(BEV_V2G_2com_pkm_bus_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(BEV_V2G_2com_pkm_bus_1)_:
+1 InvestmentFlowBlock_old_exo(BEV_V2G_2com_pkm_bus_1)
= 150

c_e_InvestmentFlowBlock_old_rule_exo(BEV_V2G_storage_BEV_V2G_bus_0)_:
+1 InvestmentFlowBlock_old_exo(BEV_V2G_storage_BEV_V2G_bus_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(BEV_V2G_storage_BEV_V2G_bus_1)_:
+1 InvestmentFlowBlock_old_exo(BEV_V2G_storage_BEV_V2G_bus_1)
= 150

c_e_InvestmentFlowBlock_old_rule_exo(el_bus_BEV_V2G_storage_0)_:
+1 InvestmentFlowBlock_old_exo(el_bus_BEV_V2G_storage_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(el_bus_BEV_V2G_storage_1)_:
+1 InvestmentFlowBlock_old_exo(el_bus_BEV_V2G_storage_1)
= 150

c_e_InvestmentFlowBlock_old_rule(wind_el_bus_0)_:
-1 InvestmentFlowBlock_old_end(wind_el_bus_0)
-1 InvestmentFlowBlock_old_exo(wind_el_bus_0)
+1 InvestmentFlowBlock_old(wind_el_bus_0)
= 0

c_e_InvestmentFlowBlock_old_rule(wind_el_bus_1)_:
+1 InvestmentFlowBlock_old(wind_el_bus_1)
-1 InvestmentFlowBlock_old_end(wind_el_bus_1)
-1 InvestmentFlowBlock_old_exo(wind_el_bus_1)
= 0

c_e_InvestmentFlowBlock_old_rule(BEV_V2G_v2g_el_bus_0)_:
-1 InvestmentFlowBlock_old_end(BEV_V2G_v2g_el_bus_0)
-1 InvestmentFlowBlock_old_exo(BEV_V2G_v2g_el_bus_0)
+1 InvestmentFlowBlock_old(BEV_V2G_v2g_el_bus_0)
= 0

c_e_InvestmentFlowBlock_old_rule(BEV_V2G_v2g_el_bus_1)_:
+1 InvestmentFlowBlock_old(BEV_V2G_v2g_el_bus_1)
-1 InvestmentFlowBlock_old_end(BEV_V2G_v2g_el_bus_1)
-1 InvestmentFlowBlock_old_exo(BEV_V2G_v2g_el_bus_1)
= 0

c_e_InvestmentFlowBlock_old_rule(BEV_V2G_2com_pkm_bus_0)_:
-1 InvestmentFlowBlock_old_end(BEV_V2G_2com_pkm_bus_0)
-1 InvestmentFlowBlock_old_exo(BEV_V2G_2com_pkm_bus_0)
+1 InvestmentFlowBlock_old(BEV_V2G_2com_pkm_bus_0)
= 0

c_e_InvestmentFlowBlock_old_rule(BEV_V2G_2com_pkm_bus_1)_:
+1 InvestmentFlowBlock_old(BEV_V2G_2com_pkm_bus_1)
-1 InvestmentFlowBlock_old_end(BEV_V2G_2com_pkm_bus_1)
-1 InvestmentFlowBlock_old_exo(BEV_V2G_2com_pkm_bus_1)
= 0

c_e_InvestmentFlowBlock_old_rule(BEV_V2G_storage_BEV_V2G_bus_0)_:
-1 InvestmentFlowBlock_old_end(BEV_V2G_storage_BEV_V2G_bus_0)
-1 InvestmentFlowBlock_old_exo(BEV_V2G_storage_BEV_V2G_bus_0)
+1 InvestmentFlowBlock_old(BEV_V2G_storage_BEV_V2G_bus_0)
= 0

c_e_InvestmentFlowBlock_old_rule(BEV_V2G_storage_BEV_V2G_bus_1)_:
+1 InvestmentFlowBlock_old(BEV_V2G_storage_BEV_V2G_bus_1)
-1 InvestmentFlowBlock_old_end(BEV_V2G_storage_BEV_V2G_bus_1)
-1 InvestmentFlowBlock_old_exo(BEV_V2G_storage_BEV_V2G_bus_1)
= 0

c_e_InvestmentFlowBlock_old_rule(el_bus_BEV_V2G_storage_0)_:
-1 InvestmentFlowBlock_old_end(el_bus_BEV_V2G_storage_0)
-1 InvestmentFlowBlock_old_exo(el_bus_BEV_V2G_storage_0)
+1 InvestmentFlowBlock_old(el_bus_BEV_V2G_storage_0)
= 0

c_e_InvestmentFlowBlock_old_rule(el_bus_BEV_V2G_storage_1)_:
+1 InvestmentFlowBlock_old(el_bus_BEV_V2G_storage_1)
-1 InvestmentFlowBlock_old_end(el_bus_BEV_V2G_storage_1)
-1 InvestmentFlowBlock_old_exo(el_bus_BEV_V2G_storage_1)
= 0

c_e_InvestmentFlowBlock_fixed(wind_el_bus_0_0)_:
+1 flow(wind_el_bus_0_0)
-1 InvestmentFlowBlock_total(wind_el_bus_0)
= 0

c_e_InvestmentFlowBlock_fixed(wind_el_bus_0_1)_:
+1 flow(wind_el_bus_0_1)
= 0

c_e_InvestmentFlowBlock_fixed(wind_el_bus_0_2)_:
+1 flow(wind_el_bus_0_2)
-1 InvestmentFlowBlock_total(wind_el_bus_0)
= 0

c_e_InvestmentFlowBlock_fixed(wind_el_bus_1_3)_:
+1 flow(wind_el_bus_1_3)
-1 InvestmentFlowBlock_total(wind_el_bus_1)
= 0

c_e_InvestmentFlowBlock_fixed(wind_el_bus_1_4)_:
+1 flow(wind_el_bus_1_4)
= 0

c_e_InvestmentFlowBlock_fixed(wind_el_bus_1_5)_:
+1 flow(wind_el_bus_1_5)
-1 InvestmentFlowBlock_total(wind_el_bus_1)
= 0

c_u_InvestmentFlowBlock_max(BEV_V2G_v2g_el_bus_0_0)_:
+1 flow(BEV_V2G_v2g_el_bus_0_0)
-1 InvestmentFlowBlock_total(BEV_V2G_v2g_el_bus_0)
<= 0

c_u_InvestmentFlowBlock_max(BEV_V2G_v2g_el_bus_0_1)_:
+1 flow(BEV_V2G_v2g_el_bus_0_1)
-1 InvestmentFlowBlock_total(BEV_V2G_v2g_el_bus_0)
<= 0

c_u_InvestmentFlowBlock_max(BEV_V2G_v2g_el_bus_0_2)_:
+1 flow(BEV_V2G_v2g_el_bus_0_2)
-1 InvestmentFlowBlock_total(BEV_V2G_v2g_el_bus_0)
<= 0

c_u_InvestmentFlowBlock_max(BEV_V2G_v2g_el_bus_1_3)_:
+1 flow(BEV_V2G_v2g_el_bus_1_3)
-1 InvestmentFlowBlock_total(BEV_V2G_v2g_el_bus_1)
<= 0

c_u_InvestmentFlowBlock_max(BEV_V2G_v2g_el_bus_1_4)_:
+1 flow(BEV_V2G_v2g_el_bus_1_4)
-1 InvestmentFlowBlock_total(BEV_V2G_v2g_el_bus_1)
<= 0

c_u_InvestmentFlowBlock_max(BEV_V2G_v2g_el_bus_1_5)_:
+1 flow(BEV_V2G_v2g_el_bus_1_5)
-1 InvestmentFlowBlock_total(BEV_V2G_v2g_el_bus_1)
<= 0

c_u_InvestmentFlowBlock_max(BEV_V2G_2com_pkm_bus_0_0)_:
+1 flow(BEV_V2G_2com_pkm_bus_0_0)
-1 InvestmentFlowBlock_total(BEV_V2G_2com_pkm_bus_0)
<= 0

c_u_InvestmentFlowBlock_max(BEV_V2G_2com_pkm_bus_0_1)_:
+1 flow(BEV_V2G_2com_pkm_bus_0_1)
-1 InvestmentFlowBlock_total(BEV_V2G_2com_pkm_bus_0)
<= 0

c_u_InvestmentFlowBlock_max(BEV_V2G_2com_pkm_bus_0_2)_:
+1 flow(BEV_V2G_2com_pkm_bus_0_2)
-1 InvestmentFlowBlock_total(BEV_V2G_2com_pkm_bus_0)
<= 0

c_u_InvestmentFlowBlock_max(BEV_V2G_2com_pkm_bus_1_3)_:
+1 flow(BEV_V2G_2com_pkm_bus_1_3)
-1 InvestmentFlowBlock_total(BEV_V2G_2com_pkm_bus_1)
<= 0

c_u_InvestmentFlowBlock_max(BEV_V2G_2com_pkm_bus_1_4)_:
+1 flow(BEV_V2G_2com_pkm_bus_1_4)
-1 InvestmentFlowBlock_total(BEV_V2G_2com_pkm_bus_1)
<= 0

c_u_InvestmentFlowBlock_max(BEV_V2G_2com_pkm_bus_1_5)_:
+1 flow(BEV_V2G_2com_pkm_bus_1_5)
-1 InvestmentFlowBlock_total(BEV_V2G_2com_pkm_bus_1)
<= 0

c_u_InvestmentFlowBlock_max(BEV_V2G_storage_BEV_V2G_bus_0_0)_:
+1 flow(BEV_V2G_storage_BEV_V2G_bus_0_0)
-1 InvestmentFlowBlock_total(BEV_V2G_storage_BEV_V2G_bus_0)
<= 0

c_u_InvestmentFlowBlock_max(BEV_V2G_storage_BEV_V2G_bus_0_1)_:
+1 flow(BEV_V2G_storage_BEV_V2G_bus_0_1)
-1 InvestmentFlowBlock_total(BEV_V2G_storage_BEV_V2G_bus_0)
<= 0

c_u_InvestmentFlowBlock_max(BEV_V2G_storage_BEV_V2G_bus_0_2)_:
+1 flow(BEV_V2G_storage_BEV_V2G_bus_0_2)
-1 InvestmentFlowBlock_total(BEV_V2G_storage_BEV_V2G_bus_0)
<= 0

c_u_InvestmentFlowBlock_max(BEV_V2G_storage_BEV_V2G_bus_1_3)_:
+1 flow(BEV_V2G_storage_BEV_V2G_bus_1_3)
-1 InvestmentFlowBlock_total(BEV_V2G_storage_BEV_V2G_bus_1)
<= 0

c_u_InvestmentFlowBlock_max(BEV_V2G_storage_BEV_V2G_bus_1_4)_:
+1 flow(BEV_V2G_storage_BEV_V2G_bus_1_4)
-1 InvestmentFlowBlock_total(BEV_V2G_storage_BEV_V2G_bus_1)
<= 0

c_u_InvestmentFlowBlock_max(BEV_V2G_storage_BEV_V2G_bus_1_5)_:
+1 flow(BEV_V2G_storage_BEV_V2G_bus_1_5)
-1 InvestmentFlowBlock_total(BEV_V2G_storage_BEV_V2G_bus_1)
<= 0

c_u_InvestmentFlowBlock_max(el_bus_BEV_V2G_storage_0_0)_:
+1 flow(el_bus_BEV_V2G_storage_0_0)
-1 InvestmentFlowBlock_total(el_bus_BEV_V2G_storage_0)
<= 0

c_u_InvestmentFlowBlock_max(el_bus_BEV_V2G_storage_0_1)_:
+1 flow(el_bus_BEV_V2G_storage_0_1)
-1 InvestmentFlowBlock_total(el_bus_BEV_V2G_storage_0)
<= 0

c_u_InvestmentFlowBlock_max(el_bus_BEV_V2G_storage_0_2)_:
+1 flow(el_bus_BEV_V2G_storage_0_2)
-1 InvestmentFlowBlock_total(el_bus_BEV_V2G_storage_0)
<= 0

c_u_InvestmentFlowBlock_max(el_bus_BEV_V2G_storage_1_3)_:
+1 flow(el_bus_BEV_V2G_storage_1_3)
-1 InvestmentFlowBlock_total(el_bus_BEV_V2G_storage_1)
<= 0

c_u_InvestmentFlowBlock_max(el_bus_BEV_V2G_storage_1_4)_:
+1 flow(el_bus_BEV_V2G_storage_1_4)
-1 InvestmentFlowBlock_total(el_bus_BEV_V2G_storage_1)
<= 0

c_u_InvestmentFlowBlock_max(el_bus_BEV_V2G_storage_1_5)_:
+1 flow(el_bus_BEV_V2G_storage_1_5)
-1 InvestmentFlowBlock_total(el_bus_BEV_V2G_storage_1)
<= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(BEV_V2G_storage_0)_:
+1 GenericInvestmentStorageBlock_total(BEV_V2G_storage_0)
-1 GenericInvestmentStorageBlock_invest(BEV_V2G_storage_0)
= 150

c_e_GenericInvestmentStorageBlock_total_storage_rule(BEV_V2G_storage_1)_:
-1 GenericInvestmentStorageBlock_total(BEV_V2G_storage_0)
+1 GenericInvestmentStorageBlock_total(BEV_V2G_storage_1)
-1 GenericInvestmentStorageBlock_invest(BEV_V2G_storage_1)
+1 GenericInvestmentStorageBlock_old(BEV_V2G_storage_1)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(BEV_V2G_storage_0)_:
+1 GenericInvestmentStorageBlock_old_end(BEV_V2G_storage_0)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(BEV_V2G_storage_1)_:
-1 GenericInvestmentStorageBlock_invest(BEV_V2G_storage_0)
+1 GenericInvestmentStorageBlock_old_end(BEV_V2G_storage_1)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_exo(BEV_V2G_storage_0)_:
+1 GenericInvestmentStorageBlock_old_exo(BEV_V2G_storage_0)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_exo(BEV_V2G_storage_1)_:
+1 GenericInvestmentStorageBlock_old_exo(BEV_V2G_storage_1)
= 150

c_e_GenericInvestmentStorageBlock_old_rule(BEV_V2G_storage_0)_:
-1 GenericInvestmentStorageBlock_old_end(BEV_V2G_storage_0)
-1 GenericInvestmentStorageBlock_old_exo(BEV_V2G_storage_0)
+1 GenericInvestmentStorageBlock_old(BEV_V2G_storage_0)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(BEV_V2G_storage_1)_:
+1 GenericInvestmentStorageBlock_old(BEV_V2G_storage_1)
-1 GenericInvestmentStorageBlock_old_end(BEV_V2G_storage_1)
-1 GenericInvestmentStorageBlock_old_exo(BEV_V2G_storage_1)
= 0

c_e_GenericInvestmentStorageBlock_initially_empty(BEV_V2G_storage_0)_:
+1 GenericInvestmentStorageBlock_storage_content(BEV_V2G_storage_0)
= 0

c_e_GenericInvestmentStorageBlock_balance(BEV_V2G_storage_0_1)_:
-1 flow(el_bus_BEV_V2G_storage_0_1)
+1 flow(BEV_V2G_storage_BEV_V2G_bus_0_1)
-0.99 GenericInvestmentStorageBlock_storage_content(BEV_V2G_storage_0)
+1 GenericInvestmentStorageBlock_storage_content(BEV_V2G_storage_1)
= 0

c_e_GenericInvestmentStorageBlock_balance(BEV_V2G_storage_0_2)_:
-1 flow(el_bus_BEV_V2G_storage_0_2)
+1 flow(BEV_V2G_storage_BEV_V2G_bus_0_2)
-0.99 GenericInvestmentStorageBlock_storage_content(BEV_V2G_storage_1)
+1 GenericInvestmentStorageBlock_storage_content(BEV_V2G_storage_2)
= 0

c_e_GenericInvestmentStorageBlock_balance(BEV_V2G_storage_1_3)_:
-1 flow(el_bus_BEV_V2G_storage_1_3)
+1 flow(BEV_V2G_storage_BEV_V2G_bus_1_3)
-0.99 GenericInvestmentStorageBlock_storage_content(BEV_V2G_storage_2)
+1 GenericInvestmentStorageBlock_storage_content(BEV_V2G_storage_3)
= 0

c_e_GenericInvestmentStorageBlock_balance(BEV_V2G_storage_1_4)_:
-1 flow(el_bus_BEV_V2G_storage_1_4)
+1 flow(BEV_V2G_storage_BEV_V2G_bus_1_4)
-0.99 GenericInvestmentStorageBlock_storage_content(BEV_V2G_storage_3)
+1 GenericInvestmentStorageBlock_storage_content(BEV_V2G_storage_4)
= 0

c_e_GenericInvestmentStorageBlock_balance(BEV_V2G_storage_1_5)_:
-1 flow(el_bus_BEV_V2G_storage_1_5)
+1 flow(BEV_V2G_storage_BEV_V2G_bus_1_5)
-0.99 GenericInvestmentStorageBlock_storage_content(BEV_V2G_storage_4)
+1 GenericInvestmentStorageBlock_storage_content(BEV_V2G_storage_5)
= 0

c_e_GenericInvestmentStorageBlock_power_coupled(BEV_V2G_storage_0)_:
+1 InvestmentFlowBlock_total(BEV_V2G_storage_BEV_V2G_bus_0)
-1 InvestmentFlowBlock_total(el_bus_BEV_V2G_storage_0)
= 0

c_e_GenericInvestmentStorageBlock_power_coupled(BEV_V2G_storage_1)_:
+1 InvestmentFlowBlock_total(BEV_V2G_storage_BEV_V2G_bus_1)
-1 InvestmentFlowBlock_total(el_bus_BEV_V2G_storage_1)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_inflow(BEV_V2G_storage_0)_:
+1 InvestmentFlowBlock_total(el_bus_BEV_V2G_storage_0)
-0.3333333333333333 GenericInvestmentStorageBlock_total(BEV_V2G_storage_0)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_inflow(BEV_V2G_storage_1)_:
+1 InvestmentFlowBlock_total(el_bus_BEV_V2G_storage_1)
-0.3333333333333333 GenericInvestmentStorageBlock_total(BEV_V2G_storage_1)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(BEV_V2G_storage_0)_:
+1 InvestmentFlowBlock_total(BEV_V2G_storage_BEV_V2G_bus_0)
-0.3333333333333333 GenericInvestmentStorageBlock_total(BEV_V2G_storage_0)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(BEV_V2G_storage_1)_:
+1 InvestmentFlowBlock_total(BEV_V2G_storage_BEV_V2G_bus_1)
-0.3333333333333333 GenericInvestmentStorageBlock_total(BEV_V2G_storage_1)
= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(BEV_V2G_storage_0_0)_:
-0.9 GenericInvestmentStorageBlock_total(BEV_V2G_storage_0)
+1 GenericInvestmentStorageBlock_storage_content(BEV_V2G_storage_0)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(BEV_V2G_storage_0_1)_:
-0.9 GenericInvestmentStorageBlock_total(BEV_V2G_storage_0)
+1 GenericInvestmentStorageBlock_storage_content(BEV_V2G_storage_1)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(BEV_V2G_storage_0_2)_:
-0.9 GenericInvestmentStorageBlock_total(BEV_V2G_storage_0)
+1 GenericInvestmentStorageBlock_storage_content(BEV_V2G_storage_2)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(BEV_V2G_storage_1_3)_:
-0.9 GenericInvestmentStorageBlock_total(BEV_V2G_storage_1)
+1 GenericInvestmentStorageBlock_storage_content(BEV_V2G_storage_3)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(BEV_V2G_storage_1_4)_:
-0.9 GenericInvestmentStorageBlock_total(BEV_V2G_storage_1)
+1 GenericInvestmentStorageBlock_storage_content(BEV_V2G_storage_4)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(BEV_V2G_storage_1_5)_:
-0.9 GenericInvestmentStorageBlock_total(BEV_V2G_storage_1)
+1 GenericInvestmentStorageBlock_storage_content(BEV_V2G_storage_5)
<= 0

bounds
   1 <= ONE_VAR_CONSTANT <= 1
   0 <= InvestmentFlowBlock_invest(el_bus_BEV_V2G_storage_0) <= +inf
   0 <= InvestmentFlowBlock_invest(el_bus_BEV_V2G_storage_1) <= +inf
   0 <= InvestmentFlowBlock_invest(wind_el_bus_0) <= +inf
   0 <= InvestmentFlowBlock_invest(wind_el_bus_1) <= +inf
   0 <= flow(el_bus_BEV_V2G_storage_0_0) <= +inf
   0 <= flow(el_bus_BEV_V2G_storage_0_1) <= +inf
   0 <= flow(el_bus_BEV_V2G_storage_0_2) <= +inf
   0 <= flow(el_bus_BEV_V2G_storage_1_3) <= +inf
   0 <= flow(el_bus_BEV_V2G_storage_1_4) <= +inf
   0 <= flow(el_bus_BEV_V2G_storage_1_5) <= +inf
   0 <= flow(BEV_V2G_2com_pkm_bus_0_0) <= +inf
   0 <= flow(BEV_V2G_2com_pkm_bus_0_1) <= +inf
   0 <= flow(BEV_V2G_2com_pkm_bus_0_2) <= +inf
   0 <= flow(BEV_V2G_2com_pkm_bus_1_3) <= +inf
   0 <= flow(BEV_V2G_2com_pkm_bus_1_4) <= +inf
   0 <= flow(BEV_V2G_2com_pkm_bus_1_5) <= +inf
   0 <= flow(BEV_V2G_storage_BEV_V2G_bus_0_0) <= +inf
   0 <= flow(BEV_V2G_bus_BEV_V2G_v2g_0_0) <= +inf
   0 <= flow(BEV_V2G_bus_BEV_V2G_2com_0_0) <= +inf
   0 <= flow(BEV_V2G_storage_BEV_V2G_bus_0_1) <= +inf
   0 <= flow(BEV_V2G_bus_BEV_V2G_v2g_0_1) <= +inf
   0 <= flow(BEV_V2G_bus_BEV_V2G_2com_0_1) <= +inf
   0 <= flow(BEV_V2G_storage_BEV_V2G_bus_0_2) <= +inf
   0 <= flow(BEV_V2G_bus_BEV_V2G_v2g_0_2) <= +inf
   0 <= flow(BEV_V2G_bus_BEV_V2G_2com_0_2) <= +inf
   0 <= flow(BEV_V2G_storage_BEV_V2G_bus_1_3) <= +inf
   0 <= flow(BEV_V2G_bus_BEV_V2G_v2g_1_3) <= +inf
   0 <= flow(BEV_V2G_bus_BEV_V2G_2com_1_3) <= +inf
   0 <= flow(BEV_V2G_storage_BEV_V2G_bus_1_4) <= +inf
   0 <= flow(BEV_V2G_bus_BEV_V2G_v2g_1_4) <= +inf
   0 <= flow(BEV_V2G_bus_BEV_V2G_2com_1_4) <= +inf
   0 <= flow(BEV_V2G_storage_BEV_V2G_bus_1_5) <= +inf
   0 <= flow(BEV_V2G_bus_BEV_V2G_v2g_1_5) <= +inf
   0 <= flow(BEV_V2G_bus_BEV_V2G_2com_1_5) <= +inf
   0 <= flow(wind_el_bus_0_0) <= +inf
   0 <= flow(BEV_V2G_v2g_el_bus_0_0) <= +inf
   0 <= flow(wind_el_bus_0_1) <= +inf
   0 <= flow(BEV_V2G_v2g_el_bus_0_1) <= +inf
   0 <= flow(wind_el_bus_0_2) <= +inf
   0 <= flow(BEV_V2G_v2g_el_bus_0_2) <= +inf
   0 <= flow(wind_el_bus_1_3) <= +inf
   0 <= flow(BEV_V2G_v2g_el_bus_1_3) <= +inf
   0 <= flow(wind_el_bus_1_4) <= +inf
   0 <= flow(BEV_V2G_v2g_el_bus_1_4) <= +inf
   0 <= flow(wind_el_bus_1_5) <= +inf
   0 <= flow(BEV_V2G_v2g_el_bus_1_5) <= +inf
   0 <= InvestmentFlowBlock_total(wind_el_bus_0) <= +inf
   0 <= InvestmentFlowBlock_total(wind_el_bus_1) <= +inf
   0 <= InvestmentFlowBlock_old(wind_el_bus_1) <= +inf
   0 <= InvestmentFlowBlock_total(BEV_V2G_v2g_el_bus_0) <= +inf
   0 <= InvestmentFlowBlock_invest(BEV_V2G_v2g_el_bus_0) <= +inf
   0 <= InvestmentFlowBlock_total(BEV_V2G_v2g_el_bus_1) <= +inf
   0 <= InvestmentFlowBlock_invest(BEV_V2G_v2g_el_bus_1) <= +inf
   0 <= InvestmentFlowBlock_old(BEV_V2G_v2g_el_bus_1) <= +inf
   0 <= InvestmentFlowBlock_total(BEV_V2G_2com_pkm_bus_0) <= +inf
   0 <= InvestmentFlowBlock_invest(BEV_V2G_2com_pkm_bus_0) <= +inf
   0 <= InvestmentFlowBlock_total(BEV_V2G_2com_pkm_bus_1) <= +inf
   0 <= InvestmentFlowBlock_invest(BEV_V2G_2com_pkm_bus_1) <= +inf
   0 <= InvestmentFlowBlock_old(BEV_V2G_2com_pkm_bus_1) <= +inf
   0 <= InvestmentFlowBlock_total(BEV_V2G_storage_BEV_V2G_bus_0) <= +inf
   0 <= InvestmentFlowBlock_invest(BEV_V2G_storage_BEV_V2G_bus_0) <= +inf
   0 <= InvestmentFlowBlock_total(BEV_V2G_storage_BEV_V2G_bus_1) <= +inf
   0 <= InvestmentFlowBlock_invest(BEV_V2G_storage_BEV_V2G_bus_1) <= +inf
   0 <= InvestmentFlowBlock_old(BEV_V2G_storage_BEV_V2G_bus_1) <= +inf
   0 <= InvestmentFlowBlock_total(el_bus_BEV_V2G_storage_0) <= +inf
   0 <= InvestmentFlowBlock_total(el_bus_BEV_V2G_storage_1) <= +inf
   0 <= InvestmentFlowBlock_old(el_bus_BEV_V2G_storage_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(wind_el_bus_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(wind_el_bus_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(BEV_V2G_v2g_el_bus_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(BEV_V2G_v2g_el_bus_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(BEV_V2G_2com_pkm_bus_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(BEV_V2G_2com_pkm_bus_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(BEV_V2G_storage_BEV_V2G_bus_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(BEV_V2G_storage_BEV_V2G_bus_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(el_bus_BEV_V2G_storage_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(el_bus_BEV_V2G_storage_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(wind_el_bus_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(wind_el_bus_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(BEV_V2G_v2g_el_bus_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(BEV_V2G_v2g_el_bus_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(BEV_V2G_2com_pkm_bus_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(BEV_V2G_2com_pkm_bus_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(BEV_V2G_storage_BEV_V2G_bus_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(BEV_V2G_storage_BEV_V2G_bus_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(el_bus_BEV_V2G_storage_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(el_bus_BEV_V2G_storage_1) <= +inf
   0 <= InvestmentFlowBlock_old(wind_el_bus_0) <= +inf
   0 <= InvestmentFlowBlock_old(BEV_V2G_v2g_el_bus_0) <= +inf
   0 <= InvestmentFlowBlock_old(BEV_V2G_2com_pkm_bus_0) <= +inf
   0 <= InvestmentFlowBlock_old(BEV_V2G_storage_BEV_V2G_bus_0) <= +inf
   0 <= InvestmentFlowBlock_old(el_bus_BEV_V2G_storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_total(BEV_V2G_storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(BEV_V2G_storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_total(BEV_V2G_storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(BEV_V2G_storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old(BEV_V2G_storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(BEV_V2G_storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(BEV_V2G_storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(BEV_V2G_storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(BEV_V2G_storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old(BEV_V2G_storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(BEV_V2G_storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(BEV_V2G_storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(BEV_V2G_storage_2) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(BEV_V2G_storage_3) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(BEV_V2G_storage_4) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(BEV_V2G_storage_5) <= +inf
end
