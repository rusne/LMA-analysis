-- keyflow_id = 1 for FW in REPAiR
-- keyflow_id = 2 for CDW in REPAiR
-- keyflow_id = 33 for CDW in CINDERELA

SELECT c."BvDid", c.name Name, c.nace NACE, c.year Year, loc.country Country,
 		   loc.city City, loc.postcode Postcode, loc.address Address,
			 (regexp_split_to_array(regexp_replace(loc.address, '\D',' ','g'), E'\\s+'))[2] AS Huisnummer
FROM asmfa_administrativelocation  AS loc RIGHT JOIN
	(SELECT b.id, b."BvDid", b.name, b.year, asmfa_activity.nace
	 FROM asmfa_activity JOIN
			(SELECT a.id, a."BvDid", a.name, a.activity_id, a.year
			 FROM actor_complete JOIN
				asmfa_actor AS a
								ON actor_complete.id = a.id
			 WHERE actor_complete.keyflow_id = 2) AS b
		ON asmfa_activity.id = b.activity_id
	 WHERE left(asmfa_activity.nace, 2) <> 'V') AS c
ON loc.actor_id = c.id;
