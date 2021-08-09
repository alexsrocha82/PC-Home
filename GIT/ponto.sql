    /* HORARIO ENTRADA / SAIDA PONTO */
  SELECT NOME_FUNCIONARIO,DATA_MARCACAO,DIA_SEMANA,BT1,BT2,BT3,BT4,BT5,BT6,
         --PT,QT,
         CASE 
                WHEN QT = 14 THEN 'ERRO' 
                WHEN QT = 42 THEN 'ERRO' 
                WHEN QT > 55 THEN 'ERRO' 
                WHEN QT = 27 AND DIA_SEMANA <> 'Sábado' THEN 'ERRO'
         ELSE 'OK'  END AS VALID
    FROM (   
        SELECT NOME_FUNCIONARIO,
               DATA_MARCACAO,
               DIA_SEMANA, 
               PT,
               COALESCE(SUBSTRING(PT from 1 for POSITION('.' in PT)-4),'') AS BT1,
               COALESCE(SUBSTRING(PT from 15 for POSITION('.' in PT)-4),'') AS BT2,
               COALESCE(SUBSTRING(PT from 29 for POSITION('.' in PT)-4),'') AS BT3,
               COALESCE(SUBSTRING(PT from 43 for POSITION('.' in PT)-4),'') AS BT4,
               COALESCE(SUBSTRING(PT from 57 for POSITION('.' in PT)-4),'') AS BT5,
               COALESCE(SUBSTRING(PT from 71 for POSITION('.' in PT)-4),'') AS BT6,
               QT
         FROM (
                SELECT NOME_FUNCIONARIO,
                       DATA_MARCACAO,
                       DIA_SEMANA,
                       LIST(PONTO) AS PT,
                       CHAR_LENGTH(LIST(PONTO)) AS QT
                 FROM (
                         SELECT DISTINCT
                                F.NOME_FUNCIONARIO,
                                M.DATA_MARCACAO,
                                S.DIA_SEMANA,
                                COALESCE(M.HORA_ENTRADA,'') || ','|| COALESCE(M.HORA_SAIDA,'') AS PONTO
                           FROM FUNCIONARIO F
                                INNER JOIN BANCO_HORAS_LANCAMENTOS    BL ON F.COD_FUNCIONARIO = BL.COD_FUNC
                                INNER JOIN MARCACAOADM                M  ON F.COD_FUNCIONARIO = M.COD_FUNCIONARIO
                                INNER JOIN DIASEMANA S ON M.COD_DIASEMANA = S.COD_DIASEMANA
                            WHERE 1=1
                              --AND F.COD_FUNCIONARIO IN ('1851','2400')  
                              AND M.DATA_MARCACAO >= '2021-01-01' 
                              ) X  
                     GROUP BY NOME_FUNCIONARIO, DATA_MARCACAO, DIA_SEMANA
                  ) A
             ) Y
            
     --------------------------------
     /*   LISTA FUNCIONARIOS   */
   ------------------------------
        
     SELECT F.COD_FUNCIONARIO, F.NOME_FUNCIONARIO, F.DATA_ADM_FUNCIONARIO, F.DATA_DEM_FUNCIONARIO,
            F.DATA_FIM_CONTRATO, F.NUM_CRACHA, F.NUN_FOLHA, F.UTILIZA_REFEICAO, F.OBS_DESCONTOS,F.ATIVO
       FROM FUNCIONARIO F
      WHERE 1=1
        --AND F.NOME_FUNCIONARIO = ''
        --AND F.COD_FUNCIONARIO IN ('1112','2400') 
        AND F.ATIVO = 'S'
        
   --------------------------------
     /*   HORAS EXTRAS   */
   ------------------------------
    SELECT 
        F.COD_FUNCIONARIO,
        F.NOME_FUNCIONARIO,
        BL.DATA,
        BL.DATA_INC,
        BL.QUANTIDADE
    FROM FUNCIONARIO                       F
        INNER JOIN BANCO_HORAS_LANCAMENTOS BL ON F.COD_FUNCIONARIO = BL.COD_FUNC
    WHERE 1=1
    AND BL.QUANTIDADE <> ''
    AND F.NOME_FUNCIONARIO LIKE '%'||'ALEX SANDRO ROCHA COUVEIRO'||'%'
    --AND F.COD_FUNCIONARIO = 2400
    ORDER BY DATA DESC 
    
    ------------------------------
    --SELECT * FROM BANCO_HORAS
--SELECT * FROM BANCO_HORAS_LANCAMENTOS WHERE BANCO_HORAS_LANCAMENTOS.COD_FUNC = '2400'
SELECT * FROM ESCALA_HORARIOS WHERE ESCALA_HORARIOS.COD_ESCALA = 167
--SELECT * FROM ESCALA
--SELECT * FROM FUNCIONARIO WHERE FUNCIONARIO.COD_FUNCIONARIO = '2400'
--SELECT * FROM CARGO
--SELECT * FROM SECAO
--SELECT * FROM SETOR
--SELECT * FROM EMPRESA    
   
       
       