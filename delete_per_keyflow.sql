--delete from asmfa_strategyfractionflow where strategy_id = 56;

-- delete from asmfa_fractionflow where keyflow_id = 1 ;
select * from asmfa_fractionflow where keyflow_id = 1 ;

-- delete from asmfa_actor2actor where keyflow_id = 1 ;
select * from asmfa_actor2actor where keyflow_id = 1 ;

-- delete from asmfa_actorstock where keyflow_id = 1 ;
select * from asmfa_actorstock where keyflow_id = 1 ;

-- delete from asmfa_productfraction where id in
select * from asmfa_productfraction where id in
                                      (select asmfa_productfraction.id
                                       from asmfa_composition join asmfa_productfraction
                                                on asmfa_composition.id = asmfa_productfraction.composition_id
                                      where asmfa_composition.keyflow_id = 1);


-- delete from asmfa_waste where composition_ptr_id in
select * from asmfa_waste where composition_ptr_id in
                              (select id
                               from asmfa_composition
                               where asmfa_composition.keyflow_id = 1);


-- delete from asmfa_product where composition_ptr_id in
select * from asmfa_product where composition_ptr_id in
                              (select id
                               from asmfa_composition
                               where asmfa_composition.keyflow_id = 1);

-- delete from asmfa_composition where keyflow_id = 1;
select * from asmfa_composition where keyflow_id = 1;

-- delete from asmfa_material where keyflow_id = 1;
select * from asmfa_material where keyflow_id = 1;

-- delete from asmfa_administrativelocation where id in
select * from asmfa_administrativelocation where id in
																							 (select asmfa_administrativelocation.id
                                                from asmfa_administrativelocation join actor_complete
                                                         on (asmfa_administrativelocation.actor_id = actor_complete.id)
                                                where actor_complete.keyflow_id = 1);

-- delete from asmfa_actor where id in
select * from asmfa_actor where id in
																							 (select asmfa_actor.id
                                                from asmfa_actor join actor_complete
                                                         using (id)
                                                where actor_complete.keyflow_id = 1);

-- delete from changes_solutionpart where implementation_flow_destination_activity_id in
-- delete from changes_affectedflow where origin_activity_id in
--                                      (select asmfa_activity.id
--                                   from asmfa_activity join asmfa_activitygroup
--                                            on (asmfa_activity.activitygroup_id = asmfa_activitygroup.id)
--                                   where asmfa_activitygroup.keyflow_id = 1);

-- delete from asmfa_activity where id in
select * from asmfa_activity where id in
																 (select asmfa_activity.id
                                  from asmfa_activity join asmfa_activitygroup
                                           on (asmfa_activity.activitygroup_id = asmfa_activitygroup.id)
                                  where asmfa_activitygroup.keyflow_id = 1);

-- delete from asmfa_activitygroup where keyflow_id = 1;
select * from asmfa_activitygroup where keyflow_id = 1;
