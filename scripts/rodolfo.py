# databases
# htc_alunos_doutorado_naturalidade
# htc_alunos_especiais_inter_posgrad_naturalidade
# htc_alunos_especiais_inter_grad_naturalidade
# htc_alunos_graduacao_naturalidade
# htc_alunos_mestrado_naturalidade
# htc_concluintes
# htc_cv_cr
# htc_fapesp
# htc_folha_unicamp
# htc_lotacao_unicamp
# htc_origem_alunos
# htc_sexo_alunos
# htc_siafem_despesas

import mysql.connector, pandas

def MergeDataFrames(VecDataFrame, DataIni, DataFim=None):
    if (DataIni>DataFim):
        aux = DataFim
        DataFim = DataIni
        DataIni = DataFim
#    for counter in range(0,len(VecDataFrame)):
        #if any("ano" in s for s in VecDataFrame[counter].columns.values):




conn = mysql.connector.connect(host='143.106.73.88', database='hackthecampus', user='htc', password='htc_123456')

dBases = ["htc_alunos_doutorado_naturalidade", "htc_alunos_especiais_inter_posgrad_naturalidade", "htc_alunos_especiais_inter_grad_naturalidade", "htc_alunos_graduacao_naturalidade", "htc_alunos_mestrado_naturalidade", "htc_concluintes", "htc_cv_cr", "htc_fapesp", "htc_folha_unicamp", "htc_lotacao_unicamp", "htc_origem_alunos", "htc_sexo_alunos", "htc_siafem_despesas"]

s = "SELECT * FROM "

dataFrame1 = pandas.read_sql(s + dBases[0], con=conn)
dataFrame2 = pandas.read_sql(s + dBases[1], con=conn)
dataFrame3 = pandas.read_sql(s + dBases[2], con=conn)
dataFrame4 = pandas.read_sql(s + dBases[3], con=conn)
dataFrame5 = pandas.read_sql(s + dBases[4], con=conn)
dataFrame6 = pandas.read_sql(s + dBases[5], con=conn)
dataFrame7 = pandas.read_sql(s + dBases[6], con=conn)
dataFrame8 = pandas.read_sql(s + dBases[7], con=conn)
dataFrame9 = pandas.read_sql(s + dBases[8], con=conn)
dataFrame10 = pandas.read_sql(s + dBases[9], con=conn)
dataFrame11 = pandas.read_sql(s + dBases[10], con=conn)
dataFrame12 = pandas.read_sql(s + dBases[11], con=conn)
dataFrame13 = pandas.read_sql(s + dBases[12], con=conn)



# cursor.close()
# connection.close()

# cnx.close()
