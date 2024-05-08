#include <stdint.h>

#define ARR_LEN 32

#define OP +

#if defined(NF_UINT8)
#define NF_IN uint8_t
#define NF_OUT uint32_t
NF_IN a[ARR_LEN] = {215, 193, 107, 66, 130, 103, 199, 77, 121, 148, 231, 128, 71, 192, 157, 63, 231, 250, 206, 230, 79, 186, 229, 174, 120, 25, 110, 155, 232, 246, 121, 220};
NF_IN b[ARR_LEN] = {66, 205, 139, 3, 183, 101, 210, 170, 0, 125, 221, 62, 82, 221, 48, 144, 60, 246, 204, 114, 20, 81, 129, 237, 27, 140, 180, 139, 207, 137, 245, 153};
NF_OUT c[ARR_LEN] = {0};
NF_OUT ref[ARR_LEN] = {281, 398, 246, 69, 313, 204, 409, 247, 121, 273, 452, 190, 153, 413, 205, 207, 291, 496, 410, 344, 99, 267, 358, 411, 147, 165, 290, 294, 439, 383, 366, 373};

#elif defined(NF_INT8)
#define NF_IN int8_t
#define NF_OUT int32_t
NF_IN a[ARR_LEN] = {21, -14, 24, -29, 18, -53, -79, -80, 28, 39, -6, -105, 65, 95, 107, 86, 101, 107, 9, -28, 51, -57, 78, 88, 100, 22, 114, 19, -13, 40, 126, 105};
NF_IN b[ARR_LEN] = {74, -106, 28, -3, 32, 87, -66, 58, -98, -71, 74, -43, 80, -102, -90, 49, -116, 18, 104, 8, 45, -121, 33, 26, 18, -28, -33, 122, -118, -122, 117, -80};
NF_OUT c[ARR_LEN] = {0};
NF_OUT ref[ARR_LEN] = {95, -120, 52, -32, 50, 34, -145, -22, -70, -32, 68, -148, 145, -7, 17, 135, -15, 125, 113, -20, 96, -178, 111, 114, 118, -6, 81, 141, -131, -82, 243, 25};

#elif defined(NF_UINT16)
#define NF_IN uint16_t
#define NF_OUT uint32_t
NF_IN a[ARR_LEN] = {8119, 13800, 52476, 61404, 1493, 27892, 6651, 17033, 14472, 42396, 22956, 11817, 33005, 2580, 6613, 64763, 13064, 23497, 47945, 54939, 60192, 11103, 44081, 63342, 3804, 44314, 55404, 22433, 16428, 39110, 28987, 11456};
NF_IN b[ARR_LEN] = {30907, 26863, 37296, 33331, 20410, 23405, 54896, 16444, 36738, 815, 48599, 22014, 2994, 18407, 15736, 62463, 23083, 18866, 23540, 62055, 41532, 40702, 46898, 25428, 27158, 42652, 99, 12603, 21915, 15690, 41771, 24814};
NF_OUT c[ARR_LEN] = {0};
NF_OUT ref[ARR_LEN] = {39026, 40663, 89772, 94735, 21903, 51297, 61547, 33477, 51210, 43211, 71555, 33831, 35999, 20987, 22349, 127226, 36147, 42363, 71485, 116994, 101724, 51805, 90979, 88770, 30962, 86966, 55503, 35036, 38343, 54800, 70758, 36270};

#elif defined(NF_INT16)
#define NF_IN int16_t
#define NF_OUT int32_t
NF_IN a[ARR_LEN] = {24602, 4465, -5609, -6405, 13226, -5359, 10629, -29702, -3581, -15779, -22434, 1806, -835, 4023, 16742, 25156, -355, -12317, -2170, 20252, 24576, 20473, -20447, 32729, 8721, -27297, 14781, 31903, -6434, 11698, -12047, -18774};
NF_IN b[ARR_LEN] = {14241, -32613, 21149, 1857, -26359, -24975, 9781, 24486, -14419, 31358, -26202, 23194, -6770, -27437, -14764, -3082, 19158, 23681, -24024, 1366, 9881, -10023, 24369, -14522, -31550, -30103, 11861, 3823, 29261, 28732, 26859, -30015};
NF_OUT c[ARR_LEN] = {0};
NF_OUT ref[ARR_LEN] = {38843, -28148, 15540, -4548, -13133, -30334, 20410, -5216, -18000, 15579, -48636, 25000, -7605, -23414, 1978, 22074, 18803, 11364, -26194, 21618, 34457, 10450, 3922, 18207, -22829, -57400, 26642, 35726, 22827, 40430, 14812, -48789};

#elif defined(NF_UINT32)
#define NF_IN uint32_t
#define NF_OUT uint32_t
NF_IN a[ARR_LEN] = {804377390, 753041788, 703689443, 764888204, 969277642, 687346378, 399914350, 577596632, 223170906, 630421209, 9553169, 162159898, 357994530, 847851410, 771482880, 363199581, 666297719, 44241330, 175943921, 1054322203, 310881386, 423904663, 588930528, 315043368, 513318029, 257382447, 51814874, 192829910, 561620909, 76088442, 432899574, 352746426};
NF_IN b[ARR_LEN] = {445303936, 106730300, 975663618, 508958618, 902854021, 1048218397, 368993088, 514415232, 751184723, 457988815, 324166002, 788932868, 960354448, 987508376, 672959147, 403266662, 1046426390, 685990584, 70689446, 90913257, 805166321, 65665923, 8429952, 422848068, 557276009, 481620758, 524650445, 628019461, 729395577, 454233672, 395492889, 1061349831};
NF_OUT c[ARR_LEN] = {0};
NF_OUT ref[ARR_LEN] = {1249681326, 859772088, 1679353061, 1273846822, 1872131663, 1735564775, 768907438, 1092011864, 974355629, 1088410024, 333719171, 951092766, 1318348978, 1835359786, 1444442027, 766466243, 1712724109, 730231914, 246633367, 1145235460, 1116047707, 489570586, 597360480, 737891436, 1070594038, 739003205, 576465319, 820849371, 1291016486, 530322114, 828392463, 1414096257};

#elif defined(NF_INT32)
#define NF_IN int32_t
#define NF_OUT int32_t
NF_IN a[ARR_LEN] = {-256713915, 297534024, -73850862, -151912583, -468303961, 390389917, 216900303, 432729451, -51956442, 189967440, -409191964, -109571486, -314357275, -491664848, 480994837, -305056099, -379723975, -324302196, -130962181, 49812238, -374376871, 524726771, 518605714, -377525459, -101031715, 193197810, 405505667, -4932851, 447800454, -190631785, -1674080, -1453211};
NF_IN b[ARR_LEN] = {182609286, -319984395, 117865294, -301965088, -171562130, 496676957, 428431617, 341577009, -498787155, -377563185, -261046059, 305121528, 367577610, 89064929, 234217076, 329698202, -465618337, -445986035, 396098326, -494548487, -295181663, -493242605, -520458617, 369318530, -181897913, -364331273, -377077201, 167593555, 503153562, 5368378, 430667619, 2607687};
NF_OUT c[ARR_LEN] = {0};
NF_OUT ref[ARR_LEN] = {-74104629, -22450371, 44014432, -453877671, -639866091, 887066874, 645331920, 774306460, -550743597, -187595745, -670238023, 195550042, 53220335, -402599919, 715211913, 24642103, -845342312, -770288231, 265136145, -444736249, -669558534, 31484166, -1852903, -8206929, -282929628, -171133463, 28428466, 162660704, 950954016, -185263407, 428993539, 1154476};

#elif defined(NF_UINT64)
#define NF_IN uint64_t
#define NF_OUT uint64_t
NF_IN a[ARR_LEN] = {2646519680808063488, 3129358038610789888, 3712914479715734016, 3494949565190595584, 4568025170226291200, 3444769841392840192, 4177176297647459328, 950490772367175168, 2469171884710180352, 2760621030186472960, 3807853544821195264, 2223817546687138816, 3648029084352676864, 1791957717901129216, 2704239441972200448, 3926004895975477248, 3680399704764602880, 3029806472256067584, 1110016799796224, 839183534234450944, 2337468968952394752, 1173486850243243520, 302622725438267392, 3965512355275040256, 4348575594307666432, 1396441022871507456, 1881905320524141568, 3735638769106584576, 287117847811061760, 2956020928702852608, 587163612856943104, 1323961283609508352};
NF_IN b[ARR_LEN] = {3827425860648246272, 256073301173927424, 165715557218501120, 1927066996362624000, 2268169957493972992, 3981384676296354304, 3307449314093576704, 3106172564916806656, 698088309732706304, 4550377915018775040, 1896049494832469504, 2821295141488195072, 1783260610181103616, 216901040255336960, 2171593181595293696, 698060554277574144, 149720518911697920, 2847256901660838400, 2905206737292154368, 485577447308484608, 2532478628837644800, 1598723860907054080, 1768185320482806784, 3580604791262115328, 2261200401398389248, 4064171045663643648, 2813680687927142912, 2154526281602320384, 2916027361418326528, 1558129048266916352, 573342295760409088, 3147612299686888448};
NF_OUT c[ARR_LEN] = {0};
NF_OUT ref[ARR_LEN] = {6473945541456309760, 3385431339784717312, 3878630036934235136, 5422016561553219584, 6836195127720264192, 7426154517689194496, 7484625611741036032, 4056663337283981824, 3167260194442886656, 7310998945205248000, 5703903039653664768, 5045112688175333888, 5431289694533780480, 2008858758156466176, 4875832623567494144, 4624065450253051392, 3830120223676300800, 5877063373916905984, 2906316754091950592, 1324760981542935552, 4869947597790039552, 2772210711150297600, 2070808045921074176, 7546117146537155584, 6609775995706055680, 5460612068535151104, 4695586008451284480, 5890165050708904960, 3203145209229388288, 4514149976969768960, 1160505908617352192, 4471573583296396800};

#elif defined(NF_INT64)
#define NF_IN int64_t
#define NF_OUT int64_t
NF_IN a[ARR_LEN] = {562798368439390720, 1330778053655493632, -1719655634880572416, 1899015370839554560, 1380467679453096448, 1922553831151740416, 1718013167781434368, 834744897910066688, 1430779504555488768, 87655742230381568, 1316586318519307776, -1433646509996138496, 1301021679889070592, -255581465109083648, 1183433439858726912, -205357286297116160, 1335353938712267776, -1958400497427141120, -2099973169817991680, 2002807194971628032, -63802211443409920, 1849615366151956992, 2051200703935209984, 767897153691876352, 331104419062739456, -1309813903259763712, -1874760035617005568, 1472945836061509120, 1792894708653544960, 1288485292620187648, 915430893652257792, -368422449025517568};
NF_IN b[ARR_LEN] = {-897841818222544384, -1782670770139317248, -341401971913253888, 304431110373190144, 1950192472719687168, 2009564177186608128, -389036314443534848, -1848313082527340032, 1262766020122064896, 1080422764326494208, -2164260347183395328, -245717091416711168, 859701765175398912, -2166873381052979200, 1933598566955552768, 2131717212163210752, 1026297390544176128, -1943647923993765376, -1981505594748238336, -649079520178903040, -2170363167434557440, -701540158174209536, -2259891056866451968, 2187431112380055040, 1471158733880547328, -1980637926306842624, 1814399112233472512, -1346713589987243008, -1361412148132348928, 801322622009213952, 2021127974489497600, -1737738072904481792};
NF_OUT c[ARR_LEN] = {0};
NF_OUT ref[ARR_LEN] = {-335043449783153664, -451892716483823616, -2061057606793826304, 2203446481212744704, 3330660152172783616, 3932118008338348544, 1328976853337899520, -1013568184617273344, 2693545524677553664, 1168078506556875776, -847674028664087552, -1679363601412849664, 2160723445064469504, -2422454846162062848, 3117032006814279680, 1926359925866094592, 2361651329256443904, -3902048421420906496, -4081478764566230016, 1353727674792724992, -2234165378877967360, 1148075207977747456, -208690352931241984, 2955328266071931392, 1802263152943286784, -3290451829566606336, -60360923383533056, 126232246074266112, 431482560521196032, 2089807914629401600, 2936558868141755392, -2106160521929999360};

#elif defined(NF_FLOAT32)
#define NF_IN float
#define NF_OUT float
NF_IN a[ARR_LEN] = {-0.9856308698654175, -0.26173970103263855, -0.9506999850273132, 0.2096964716911316, 0.7183512449264526, -0.6260166168212891, -0.7752179503440857, -0.3111007809638977, 0.9183430671691895, -0.7396845817565918, 0.9330385327339172, -0.2755202651023865, -0.053259193897247314, -0.4147360324859619, 0.8742536902427673, 0.9162957668304443, 0.2718314230442047, -0.6319088935852051, 0.9859035611152649, -0.7948391437530518, 0.16169875860214233, -0.6871938705444336, 0.7953506112098694, 0.8913567662239075, 0.6087806224822998, -0.3682171702384949, -0.5143226385116577, 0.509716808795929, -0.41788095235824585, -0.1604292392730713, -0.9074886441230774, -0.7355324029922485};
NF_IN b[ARR_LEN] = {-0.9589007496833801, -0.8441577553749084, -0.8535776734352112, -0.15953660011291504, 0.10155435651540756, 0.48175764083862305, -0.7154330611228943, -0.15562251210212708, 0.2739320695400238, -0.8308886289596558, -0.11037769168615341, -0.2614879310131073, 0.8978638648986816, -0.8842857480049133, -0.18274755775928497, -0.16554903984069824, 0.45636099576950073, -0.35865798592567444, -0.5920194387435913, -0.41337668895721436, -0.05822491645812988, 0.9005366563796997, 0.593034029006958, -0.4460594952106476, 0.11636317521333694, 0.3764006197452545, 0.5913143157958984, -0.10767123103141785, -0.20244619250297546, 0.5352814793586731, -0.13656701147556305, -0.5040846467018127};
NF_OUT c[ARR_LEN] = {0};
NF_OUT ref[ARR_LEN] = {-1.9445316791534424, -1.1058974266052246, -1.8042776584625244, 0.05015987157821655, 0.8199055790901184, -0.14425897598266602, -1.49065101146698, -0.4667232930660248, 1.1922751665115356, -1.5705732107162476, 0.8226608633995056, -0.5370081663131714, 0.8446046710014343, -1.2990217208862305, 0.6915061473846436, 0.7507467269897461, 0.7281924486160278, -0.9905668497085571, 0.3938841223716736, -1.2082158327102661, 0.10347384214401245, 0.2133427858352661, 1.3883845806121826, 0.4452972710132599, 0.7251437902450562, 0.008183449506759644, 0.07699167728424072, 0.4020455777645111, -0.6203271150588989, 0.3748522400856018, -1.044055700302124, -1.239617109298706};

#elif defined(NF_FLOAT64)
#define NF_IN double
#define NF_OUT double
NF_IN a[ARR_LEN] = {-0.09310593693870461, 0.8742092925809122, -0.7148650235627974, -0.07512929094557586, 0.2746070487275629, -0.03342402346379947, -0.5927201912592601, -0.9963136787686682, 0.397983423606878, 0.237471036046905, -0.9844467011282716, -0.4028797579637584, 0.537268519085683, 0.2578407570892418, 0.09041623188794445, -0.6875577803819022, 0.4125880859993769, -0.0571301565683926, 0.3563574924719273, 0.5201796734469843, -0.5352745571175097, 0.5239900261954233, -0.4398232306232215, 0.968030274236491, -0.7583367784309627, 0.7674360374881128, -0.9189057499132574, -0.48684836330371195, 0.05220381752493686, 0.1632323668891893, -0.20753002994381564, -0.7959365435458579};
NF_IN b[ARR_LEN] = {-0.49478382835057344, -0.4332069922790227, 0.510445709117463, 0.8175486504440141, 0.19081983097283883, -0.9290980686179451, 0.5844729432834206, -0.38879213432016013, -0.3202191871675131, 0.06037087529082941, -0.5019059048488899, 0.8399561757147394, -0.6728904833183742, -0.17033919899253447, -0.42061610098558844, 0.03966820440322927, 0.14796360616475313, 0.25427937820968527, 0.06275160767594556, -0.17839099532880098, 0.2691880247529319, -0.19317424682636486, 0.5571005181080955, 0.5763548505099803, -0.41549166377835567, -0.25639135288845094, 0.2576218118937723, -0.6858600657686857, 0.3940638619738497, -0.23714449403857385, 0.18212494951401403, -0.7209338015375564};
NF_OUT c[ARR_LEN] = {0};
NF_OUT ref[ARR_LEN] = {-0.587889765289278, 0.44100230030188947, -0.20441931444533434, 0.7424193594984383, 0.46542687970040175, -0.9625220920817446, -0.008247247975839533, -1.3851058130888283, 0.07776423643936492, 0.2978419113377344, -1.4863526059771615, 0.43707641775098094, -0.13562196423269124, 0.08750155809670734, -0.330199869097644, -0.6478895759786729, 0.56055169216413, 0.19714922164129267, 0.41910910014787284, 0.34178867811818336, -0.2660865323645778, 0.3308157793690585, 0.11727728748487398, 1.5443851247464713, -1.1738284422093184, 0.5110446845996619, -0.661283938019485, -1.1727084290723977, 0.44626767949878654, -0.07391212714938455, -0.025405080429801608, -1.5168703450834142};

#else
_Static_assert(0, "NF not defined");
#endif