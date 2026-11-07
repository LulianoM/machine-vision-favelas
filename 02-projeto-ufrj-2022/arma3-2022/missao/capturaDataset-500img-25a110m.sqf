/*
  capturaDataset.sqf  (2026-09-11)
  Gera um dataset sintético aéreo no ARMA 3 com anotação automática de bounding box 2D.

  Uso:
    1. Crie uma missão no editor Eden com um jogador e um ou mais marcadores
       chamados ds_centro_1, ds_centro_2, ... nos pontos onde as cenas devem acontecer
       (ruas, becos, pátios entre casas).
    2. Salve a missão. Copie este arquivo para a pasta da missão
       (Documents\Arma 3\missions\<nome>.<mapa>\  ou  ...\mpmissions\...).
    3. Crie init.sqf na mesma pasta com a linha:   [] execVM "capturaDataset.sqf";
    4. Rode a missão (Play). O script muda clima, hora, unidades e câmera a cada
       iteração, salva um PNG em Documents\Arma 3\Screenshots\ e escreve as anotações
       no arquivo .rpt (%LOCALAPPDATA%\Arma 3\arma3_*.rpt) em linhas DSIMG e DSLBL.
    5. Depois rode rpt_to_yolo.py e preview_boxes.py.

  Classes: 0 = pessoa_armada, 1 = pessoa_desarmada.

  Sobre o boundingBoxReal: retorna a caixa 3D no espaço do modelo. Aqui os 8 cantos
  são levados ao mundo (modelToWorldVisual) e depois à tela (worldToScreen). O min/max
  dos cantos projetados é a caixa 2D. worldToScreen devolve coordenadas de UI
  (espaço safeZone); a conversão para fração da tela usa safeZoneX/Y/W/H.
  Se as caixas do preview saírem deslocadas, troque DS_USA_SAFEZONE para false.
*/

if (!hasInterface) exitWith {};

// ---------------- PARÂMETROS ----------------
DS_N_IMAGENS      = 500;
DS_PREFIXO        = "ds";
DS_MIN_UNIDADES   = 1;
DS_MAX_UNIDADES   = 8;
DS_RAIO_CENA      = 25;      // metros em torno do centro para espalhar unidades
DS_ALT_MIN        = 25;      // altitude da câmera em metros (acima do terreno)
DS_ALT_MAX        = 110;
DS_PITCH_MIN      = 45;      // 90 = câmera apontando para baixo (nadir)
DS_PITCH_MAX      = 89;
DS_FOV_MIN        = 0.45;
DS_FOV_MAX        = 0.90;
DS_PROB_ARMADO    = 0.5;     // probabilidade de spawnar classe militar/bandido
DS_PROB_CIVIL_ARM = 0.3;     // probabilidade de um civil receber arma (ameaça sem uniforme)
DS_MIN_VIS        = 0.35;    // visibilidade mínima câmera->unidade para anotar (0..1)
DS_MIN_LADO       = 0.004;   // caixa menor que isso (fração da tela) é descartada
DS_ESPERA_FRAME   = 0.6;     // segundos para o motor renderizar antes de medir
DS_ESPERA_SCREEN  = 1.2;     // segundos após o screenshot
DS_USA_SAFEZONE   = true;
DS_CENTROS        = [];      // opcional: [[x,y,z],...]; se vazio usa os marcadores ds_centro_*

DS_CLASSES_ARMADAS = [
  "O_G_Soldier_F","O_G_Soldier_lite_F","O_G_Soldier_SL_F",
  "I_G_Soldier_F","I_G_Soldier_lite_F","B_G_Soldier_F","B_G_Soldier_lite_F",
  "O_Soldier_F","O_Soldier_lite_F","I_Soldier_F","B_Soldier_F",
  "I_C_Soldier_Bandit_1_F","I_C_Soldier_Bandit_2_F","I_C_Soldier_Bandit_3_F"
];
DS_CLASSES_CIVIS = [
  "C_man_1","C_man_1_1_F","C_man_1_2_F","C_man_1_3_F",
  "C_man_polo_1_F","C_man_polo_2_F","C_man_polo_3_F","C_man_polo_4_F",
  "C_man_shorts_1_F","C_man_shorts_2_F","C_man_shorts_3_F",
  "C_Man_casual_1_F","C_Man_casual_2_F","C_Man_casual_3_F",
  "C_man_sport_1_F","C_man_sport_2_F","C_man_hunter_1_F","C_man_w_worker_F"
];
DS_ARMAS_CIVIL = ["arifle_MX_F","arifle_Katiba_F","SMG_01_F","SMG_02_F","arifle_TRG20_F"];

// ---------------- SETUP ----------------
private _centros = +DS_CENTROS;
if (_centros isEqualTo []) then {
  {
    if ((toLower _x) find "ds_centro" == 0) then { _centros pushBack (getMarkerPos _x); };
  } forEach allMapMarkers;
};
if (_centros isEqualTo []) then {
  _centros = [getPos player];
  hint "capturaDataset: sem centros; usando a posicao do jogador. Para varias cenas, crie marcadores ds_centro_1, ds_centro_2... no editor.";
};

private _res = getResolution;
private _w = _res select 0;
private _h = _res select 1;

showHUD [false,false,false,false,false,false,false,false];
showCinemaBorder false;
enableRadio false;
enableSentences false;

private _grp = createGroup [civilian, true];
private _cam = "camera" camCreate [0,0,50];
_cam cameraEffect ["internal","back"];
_cam camSetFov 0.7;
_cam camCommit 0;

private _unidades = [];

// bbox 2D normalizada [x1,y1,x2,y2] em fração da tela, ou [] se não coube na tela
DS_fnc_bbox2D = {
  params ["_obj"];
  private _bb = boundingBoxReal _obj;
  private _a = _bb select 0;
  private _b = _bb select 1;
  private _cantos = [
    [_a select 0, _a select 1, _a select 2], [_b select 0, _a select 1, _a select 2],
    [_a select 0, _b select 1, _a select 2], [_b select 0, _b select 1, _a select 2],
    [_a select 0, _a select 1, _b select 2], [_b select 0, _a select 1, _b select 2],
    [_a select 0, _b select 1, _b select 2], [_b select 0, _b select 1, _b select 2]
  ];
  private _xs = [];
  private _ys = [];
  {
    private _s = worldToScreen (_obj modelToWorldVisual _x);
    if (count _s == 2) then {
      if (DS_USA_SAFEZONE) then {
        _xs pushBack (((_s select 0) - safeZoneX) / safeZoneW);
        _ys pushBack (((_s select 1) - safeZoneY) / safeZoneH);
      } else {
        _xs pushBack (_s select 0);
        _ys pushBack (_s select 1);
      };
    };
  } forEach _cantos;
  if (count _xs < 8) exitWith { [] };
  private _x1 = 0 max (selectMin _xs);
  private _x2 = 1 min (selectMax _xs);
  private _y1 = 0 max (selectMin _ys);
  private _y2 = 1 min (selectMax _ys);
  if ((_x2 - _x1) < DS_MIN_LADO || (_y2 - _y1) < DS_MIN_LADO) exitWith { [] };
  [_x1, _y1, _x2, _y2]
};

diag_log format ["DSRUN|inicio|%1|%2x%3|safeZone=%4,%5,%6,%7|mapa=%8", DS_N_IMAGENS, _w, _h, safeZoneX, safeZoneY, safeZoneW, safeZoneH, worldName];

// ---------------- LOOP ----------------
for "_i" from 1 to DS_N_IMAGENS do {

  { deleteVehicle _x } forEach _unidades;
  _unidades = [];

  // hora e clima (domain randomization)
  private _hora = selectRandom [6, 7, 8, 10, 12, 14, 16, 17, 18];
  setDate [2024, selectRandom [1, 4, 7, 10], 15, _hora, floor random 60];
  0 setOvercast (random 0.85);
  0 setFog (random 0.12);
  0 setRain (if (random 1 < 0.15) then { random 0.5 } else { 0 });
  forceWeatherChange;

  // unidades
  private _centro = selectRandom _centros;
  private _n = DS_MIN_UNIDADES + floor random (DS_MAX_UNIDADES - DS_MIN_UNIDADES + 1);
  for "_k" from 1 to _n do {
    private _armado = (random 1) < DS_PROB_ARMADO;
    private _cls = if (_armado) then { selectRandom DS_CLASSES_ARMADAS } else { selectRandom DS_CLASSES_CIVIS };
    private _pos = _centro getPos [random DS_RAIO_CENA, random 360];
    private _u = _grp createUnit [_cls, _pos, [], 0, "CAN_COLLIDE"];
    if (isNull _u) then { continue };
    _u setDir (random 360);
    _u disableAI "ALL";
    _u allowDamage false;
    _u setUnitPos (selectRandom ["UP", "UP", "UP", "MIDDLE", "DOWN"]);
    if (!_armado && (random 1) < DS_PROB_CIVIL_ARM) then {
      private _arma = selectRandom DS_ARMAS_CIVIL;
      _u addWeapon _arma;
      _u selectWeapon _arma;
    };
    _unidades pushBack _u;
  };

  // câmera
  private _alt   = DS_ALT_MIN + random (DS_ALT_MAX - DS_ALT_MIN);
  private _pitch = DS_PITCH_MIN + random (DS_PITCH_MAX - DS_PITCH_MIN);
  private _dir   = random 360;
  private _alvo  = _centro getPos [random 8, random 360];
  private _distH = _alt / (tan _pitch);
  private _camPos = _alvo getPos [_distH, _dir];
  _camPos set [2, _alt];
  _cam camSetPos _camPos;
  _cam camSetTarget [_alvo select 0, _alvo select 1, 0];
  _cam camSetFov (DS_FOV_MIN + random (DS_FOV_MAX - DS_FOV_MIN));
  _cam camCommit 0;
  waitUntil { camCommitted _cam };
  sleep DS_ESPERA_FRAME;

  // nome do arquivo
  private _num = str _i;
  while { count _num < 6 } do { _num = "0" + _num };
  private _nome = format ["%1_%2.png", DS_PREFIXO, _num];

  // anotações (mede antes do screenshot, mesma câmera)
  private _linhas = [];
  {
    private _u = _x;
    private _vis = [_cam, "VIEW", _u] checkVisibility [getPosASL _cam, aimPos _u];
    if (_vis >= DS_MIN_VIS) then {
      private _bb = [_u] call DS_fnc_bbox2D;
      if (count _bb == 4) then {
        private _classe = if ((primaryWeapon _u) != "" || (handgunWeapon _u) != "") then { 0 } else { 1 };
        _linhas pushBack format ["DSLBL|%1|%2|%3|%4|%5|%6|%7", _nome, _classe, _bb select 0, _bb select 1, _bb select 2, _bb select 3, typeOf _u];
      };
    };
  } forEach _unidades;

  screenshot _nome;
  diag_log format ["DSIMG|%1|%2|%3|%4|%5|%6|%7|%8|%9", _nome, _w, _h, _alt, _pitch, _hora, overcast, fog, count _linhas];
  { diag_log _x } forEach _linhas;

  hintSilent format ["capturaDataset %1/%2  (%3 anotações)", _i, DS_N_IMAGENS, count _linhas];
  sleep DS_ESPERA_SCREEN;
};

{ deleteVehicle _x } forEach _unidades;
_cam cameraEffect ["terminate", "back"];
camDestroy _cam;
showHUD true;
diag_log "DSRUN|fim";
hint "capturaDataset: concluído.";
