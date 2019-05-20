from os import path
import tempfile

# Flask
APP_NAME = 'eKTAB'
DEBUG = True
SERVER_HOST = 'localhost'
SERVER_PORT = 4041
SECRET_KEY = '8lsbAgXecB'

# Localization
CURRENT_TIMEZONE = 'Asia/Riyadh'
FALLBACK_LOCALE = 'en'

# Paths
APP_ROOT = path.dirname(path.abspath(__file__))
UPLOAD_PATH = path.join(APP_ROOT, '_files')
ALLOWED_EXTENSIONS = set(['csv'])

# DB Statements

DB_QUERIES = [
        {'ActorQuery': "SELECT c.Name,  c.Act_i as id , c.\"Desc\", a.Turn_t, a.Dim_k , a.Pos_Coord , b.Sal, b.scenarioid, d.Scenario from actordescription c, VectorPosition a, SpatialSalience b, scenarioDesc d where c.Act_i = a.Act_i and c.Act_i = b.Act_i and a.ScenarioId = b.ScenarioId and c.ScenarioId = b.ScenarioId and d.ScenarioId = b.ScenarioId and a.Act_i = b.Act_i and a.Turn_t = b.Turn_t and a.Dim_k = b.Dim_k"},
        {'BargainQuery': "SELECT M.Movd_Turn as turn, MN.Name as Moved_Name, M.Dim_k, M.PrevPos, M.CurrPos,M.Diff , M.Mover_BargnID as BargnID , MI.Name as Initiator, MR.Name as Receiver ,B.scenarioid \
                            from ( select L0.Act_i, L0.Dim_k, L0.Turn_t as Movd_Turn, L0.Mover_BargnId, L0.scenarioid, L1.scenarioid, \
                            L0.Pos_Coord as CurrPos, L1.Pos_Coord as PrevPos, L0.Pos_Coord - L1.Pos_Coord as Diff \
                            from (select * from VectorPosition where Turn_t <> 0 ) \
                            as L0 inner join (select * from VectorPosition ) \
                            as L1 on L0.Turn_t = (L1.Turn_t+1) and L0.Act_i = L1.Act_i and L0.Dim_k = L1.Dim_k and L0.scenarioid = L1.scenarioid \
                            where L0.Pos_Coord <> L1.Pos_Coord ) as M inner join Bargn as B on M.Mover_BargnId = B.BargnId and M.scenarioid = B.scenarioid \
                            inner join ( select Act_i,scenarioid, name from ActorDescription ) as MI \
                            on B.Init_Act_i = MI.Act_i and MI.scenarioid = B.scenarioid inner join ( select Act_i, scenarioid, name from ActorDescription \
                            ) as MR on B.Recd_Act_j = MR.Act_i and MR.scenarioid = B.scenarioid inner join \
                            ActorDescription as MN on M.Act_i = MN.Act_i and MN.scenarioid = B.scenarioid ORDER BY M.Dim_k" },
        {'PowerQuery': "SELECT distinct d.scenarioid, c.Act_i, c.Name , d.Cap * b.Sal as fpower, b.Dim_k  from SpatialCapability d, ActorDescription c, SpatialSalience b \
                            where c.Act_i = b.Act_i and b.Act_i = d.Act_i and b.Turn_t = d.Turn_t and d.ScenarioId = b.ScenarioId and d.ScenarioId = c.ScenarioId "},
        {'NetworkActorQuery': "SELECT c.Act_i as id, Name as name, a.Turn_t, a.Dim_k,  b.scenarioid from actordescription c, VectorPosition a, \
                            SpatialSalience b where c.Act_i = a.Act_i and c.Act_i = b.Act_i and a.ScenarioId = b.ScenarioId and b.ScenarioId = c.ScenarioId and b.ScenarioId = {scenarioID} \
                            and a.Dim_k = b.Dim_k and b.Dim_k = {dimID} and a.Turn_t = b.Turn_t and b.Turn_t= {turnID} and b.scenarioid = {scenarioID}"},
        {'NetworkQuery': "SELECT B.ScenarioID, B.Turn_t, B.BargnID, B.Init_Act_i, B.Recd_Act_j,M.Dim_k, AI.Name as Init, AR.Name as Rcvr, \
                            B.Init_Prob, B.Recd_Prob from Bargn as B inner join ActorDescription as AI on B.Init_Act_i = AI.Act_i and B.ScenarioID = AI.ScenarioID inner join \
                            ActorDescription as AR on B.Recd_Act_j = AR.Act_i and B.ScenarioID = AR.ScenarioID inner join \
                            VectorPosition as M on M.Act_i = B.Init_Act_i and M.ScenarioId = B.ScenarioID  and M.Turn_t = B.Turn_t  \
                            where M.Turn_t = {turnID} and M.Dim_k = {dimID} and M.ScenarioId = {scenarioID} \
                            order by B.Turn_t, BargnID "},
        {'NetworkBargainQuery': "SELECT B.*, M.Dim_k, AI.Name as Init, AR.Name as Rcvr \
                            from (select ScenarioId, Turn_t, BargnId, Init_Act_i, Recd_Act_j \
                            ,'Init' as Q from Bargn where Init_Seld = 1 union select ScenarioId, \
                            Turn_t, BargnId, Init_Act_i, Recd_Act_j ,'Rcvr' from Bargn  \
                            where Recd_Seld = 1 ) as B inner join  ActorDescription as AI on \
                            B.Init_Act_i = AI.Act_i and B.ScenarioID = AI.ScenarioID inner join \
                            ActorDescription as AR on B.Recd_Act_j = AR.Act_i and \
                            B.ScenarioID = AR.ScenarioID inner join \
                            VectorPosition as M on M.Act_i = B.Init_Act_i and M.ScenarioId = B.ScenarioID  and M.Turn_t = B.Turn_t \
                            where B.Turn_t = {turnID} and M.ScenarioId = {scenarioID} and M.Dim_k = {dimID}" },
        {'InitialScenario': "SELECT s.Scenario, d.ScenarioId, d.Dim_k, d.'Desc' \
                            FROM DimensionDescription d, ScenarioDesc s where s.ScenarioId = d.ScenarioId" },
        {'Dimension': "SELECT ScenarioId, Dim_k, Desc FROM DimensionDescription"},
        {'Dimension_By_DimID': "SELECT ScenarioId, Dim_k, Desc FROM DimensionDescription where Dim_k = {dimID}"},
        {'Dimension_By_ScenarioID': "SELECT ScenarioId, Dim_k, Desc FROM DimensionDescription where ScenarioId = '{scenarioID}'"},
        {'Dimension_By_Scenario_and_DimID': "SELECT ScenarioId, Dim_k, Desc FROM DimensionDescription where ScenarioId = '{scenarioID}' and Dim_k = {dimID}"},
        {'Scenario': "SELECT ScenarioId, Scenario, Desc FROM ScenarioDesc"},
        {'StackedBarQuery': "SELECT c.Name, a.Turn_t, a.Pos_Coord, d.Cap * b.Sal as fpower \
                            from actordescription c, VectorPosition a, SpatialSalience b, SpatialCapability d \
                            where c.Act_i = a.Act_i and c.Act_i = b.Act_i and a.ScenarioId = b.ScenarioId and c.ScenarioId = b.ScenarioId and d.ScenarioId = b.ScenarioId and a.Act_i = b.Act_i and a.Turn_t = b.Turn_t and a.Dim_k = b.Dim_k and \
                            a.Turn_t = {turnID} and c.ScenarioId = '{scenarioID}' and a.Dim_k = {dimID} \
                            Group by c.Name, a.Turn_t, a.Pos_Coord Order by a.Pos_Coord asc" },
        {'LineChartQuery': "SELECT M.Movd_Turn as turn, MN.Name as Moved_Name, M.Dim_k, M.PrevPos, M.CurrPos,M.Diff , M.Mover_BargnID as BargnID , MI.Name as Initiator, MR.Name as Receiver ,B.scenarioid \
                            from ( select L0.Act_i, L0.Dim_k, L0.Turn_t as Movd_Turn, L0.Mover_BargnId, L0.scenarioid, L1.scenarioid, \
                            L0.Pos_Coord as CurrPos, L1.Pos_Coord as PrevPos, L0.Pos_Coord - L1.Pos_Coord as Diff \
                            from (select * from VectorPosition where Turn_t <> 0 ) \
                            as L0 inner join (select * from VectorPosition ) \
                            as L1 on L0.Turn_t = (L1.Turn_t+1) and L0.Act_i = L1.Act_i and L0.Dim_k = L1.Dim_k and L0.scenarioid = L1.scenarioid \
                            where L0.Pos_Coord <> L1.Pos_Coord ) as M inner join Bargn as B on M.Mover_BargnId = B.BargnId and M.scenarioid = B.scenarioid \
                            inner join ( select Act_i,scenarioid, name from ActorDescription ) as MI \
                            on B.Init_Act_i = MI.Act_i and MI.scenarioid = B.scenarioid inner join ( select Act_i, scenarioid, name from ActorDescription \
                            ) as MR on B.Recd_Act_j = MR.Act_i and MR.scenarioid = B.scenarioid inner join \
                            ActorDescription as MN on M.Act_i = MN.Act_i and MN.scenarioid = B.scenarioid \
                            ORDER BY M.Dim_k" }
]

# Where M.Dim_k = {dimID} and ScenarioId = '{scenarioID}'and M.Movd_Turn = {turnID}