SELECT 
  pte.id as entrega_id,
  pte.forca_trabalho as entrega_forca_trabalho,
  pte.descricao as entrega_descricao,
  pee.id as plano_entrega_id,
  pee.descricao as plano_entrega_descricao,
  pt.numero as plano_trabalho_numero,
  pt.data_inicio as plano_trabalho_data_inicio,
  pt.data_fim as plano_trabalho_data_fim,
  pt.status as plano_trabalho_status
from {DB_NAME}.planos_trabalhos_entregas pte  
inner join {DB_NAME}.planos_trabalhos pt on pt.id = pte.plano_trabalho_id  
inner join {DB_NAME}.usuarios u on pt.usuario_id = u.id 
left join {DB_NAME}.planos_entregas_entregas pee on (pee.id = pte.plano_entrega_entrega_id)
where 
u.cod_jornada < 99
AND pt.status in (
  'ATIVO',
  'AGUARDANDO_ASSINATURA',
  'INCLUIDO'
)
and u.cpf = :cpf
and pte.deleted_at is null
and pt.deleted_at is null
and pee.deleted_at is null
ORDER BY pt.numero, pee.descricao ASC;