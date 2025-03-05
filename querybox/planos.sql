SELECT 
  pt.id as plano_trablho_id,
  pt.numero as plano_trabalho_numero,
  pt.data_inicio as plano_trabalho_data_inicio,
  pt.data_fim as plano_trabalho_data_fim,
  pt.status as plano_trabalho_status,
  u.apelido as usuario_apelido,
  u.nome as usuario_nome,
  CONCAT(SUBSTRING(u.cpf, 1, 3), '.***.***-**') AS usuario_cpf_mascarado,
  u.telefone as usuario_telefone,
    CASE 
        WHEN LOCATE('petrvs.gov.br', u.email) = 0 THEN u.email 
        ELSE NULL 
    END AS usuario_email_filtrado,
  un.nome as unidade_nome,
  un.sigla as unidade_sigla,
  un.codigo as unidade_codigoo,
  tm.nome as modalidade_nome,
  pg.nome as programa_nome,
  pg.data_inicio as programa_data_inicio,
  pg.data_fim as programa_data_fim,
  un_inst.nome as programa_unidade_instituidora_nome,
  un_aut.nome as programa_unidade_autorizadora_nome
  #documento
from {DB_NAME}.planos_trabalhos pt 
inner join {DB_NAME}.usuarios u on pt.usuario_id = u.id 
inner join {DB_NAME}.unidades un on pt.unidade_id = un.id 
inner join {DB_NAME}.tipos_modalidades tm on pt.tipo_modalidade_id = tm.id
inner join {DB_NAME}.programas pg on pg.id = pt.programa_id 
inner join {DB_NAME}.unidades un_inst on pg.unidade_id = un_inst.id 
inner join {DB_NAME}.unidades un_aut on pg.unidade_id = un_aut.id 
#inner join {DB_NAME}.documentos d on pt.documento_id = d.id   
where 
u.cod_jornada < 99
AND pt.status in (
  'ATIVO',
  'AGUARDANDO_ASSINATURA',
  'CONCLUIDO',
  'INCLUIDO'
)
AND pt.data_inicio >= :data_inicio 
AND pt.data_fim < :data_fim
ORDER BY u.nome, pt.created_at DESC;