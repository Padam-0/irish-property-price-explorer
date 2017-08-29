var na_sales_cached = [[1264896000000, 270426.61], [1267315200000, 265245.65], [1269993600000, 253996.98], [1272585600000, 249546.33], [1275264000000, 243940.49], [1277856000000, 251675.02], [1280534400000, 245919.38], [1283212800000, 253303.13], [1285804800000, 244117.27], [1288483200000, 237504.44], [1291075200000, 220655.84], [1293753600000, 235261.04], [1296432000000, 243739.39], [1298851200000, 239728.19], [1301529600000, 234299.53], [1304121600000, 223505.47], [1306800000000, 222498.9], [1309392000000, 215064.31], [1312070400000, 220945.69], [1314748800000, 235617.45], [1317340800000, 214935.61], [1320019200000, 213972.29], [1322611200000, 210572.57], [1325289600000, 203785.79], [1327968000000, 216221.71], [1330473600000, 194925.86], [1333152000000, 194016.48], [1335744000000, 186529.93], [1338422400000, 200449.82], [1341014400000, 189132.93], [1343692800000, 207835.63], [1346371200000, 212885.5], [1348963200000, 204428.68], [1351641600000, 192424.98], [1354233600000, 190303.27], [1356912000000, 203955.87], [1359590400000, 182520.45], [1362009600000, 195620.5], [1364688000000, 190044.67], [1367280000000, 200125.26], [1369958400000, 184106.13], [1372550400000, 205676.53], [1375228800000, 201949.32], [1377907200000, 216518.61], [1380499200000, 204317.71], [1383177600000, 211843.46], [1385769600000, 218019.76], [1388448000000, 198953.12], [1391126400000, 193341.39], [1393545600000, 193852.78], [1396224000000, 182002.04], [1398816000000, 193576.0], [1401494400000, 206890.23], [1404086400000, 208970.42], [1406764800000, 208064.59], [1409443200000, 231494.84], [1412035200000, 232502.18], [1414713600000, 220695.53], [1417305600000, 218144.27], [1419984000000, 193059.2], [1422662400000, 227256.64], [1425081600000, 206937.05], [1427760000000, 202768.05], [1430352000000, 205386.35], [1433030400000, 207664.89], [1435622400000, 210550.45], [1438300800000, 228356.29], [1440979200000, 241669.47], [1443571200000, 223591.28], [1446249600000, 234158.73], [1448841600000, 222067.73], [1451520000000, 215409.56], [1454198400000, 241352.34], [1456704000000, 221261.12], [1459382400000, 230067.76], [1461974400000, 231385.28], [1464652800000, 228355.02], [1467244800000, 231104.54], [1469923200000, 243028.29], [1472601600000, 256081.52], [1475193600000, 252918.11], [1477872000000, 247103.34], [1480464000000, 247510.68], [1483142400000, 249263.71], [1485820800000, 267239.44], [1488240000000, 255160.53], [1490918400000, 267328.09]];
var na_volume_cached = [[1264896000000, 1055.0], [1267315200000, 1346.0], [1269993600000, 1578.0], [1272585600000, 1579.0], [1275264000000, 1585.0], [1277856000000, 1750.0], [1280534400000, 2070.0], [1283212800000, 1818.0], [1285804800000, 1847.0], [1288483200000, 1747.0], [1291075200000, 1644.0], [1293753600000, 1918.0], [1296432000000, 990.0], [1298851200000, 1075.0], [1301529600000, 1265.0], [1304121600000, 1115.0], [1306800000000, 1316.0], [1309392000000, 1425.0], [1312070400000, 1581.0], [1314748800000, 1446.0], [1317340800000, 1688.0], [1320019200000, 1454.0], [1322611200000, 1840.0], [1325289600000, 2101.0], [1327968000000, 1141.0], [1330473600000, 1320.0], [1333152000000, 1473.0], [1335744000000, 1322.0], [1338422400000, 1769.0], [1341014400000, 1910.0], [1343692800000, 2115.0], [1346371200000, 2069.0], [1348963200000, 1866.0], [1351641600000, 2192.0], [1354233600000, 2853.0], [1356912000000, 3576.0], [1359590400000, 1434.0], [1362009600000, 1432.0], [1364688000000, 1701.0], [1367280000000, 1703.0], [1369958400000, 2066.0], [1372550400000, 1987.0], [1375228800000, 2701.0], [1377907200000, 2426.0], [1380499200000, 2568.0], [1383177600000, 2872.0], [1385769600000, 2807.0], [1388448000000, 4571.0], [1391126400000, 1838.0], [1393545600000, 2222.0], [1396224000000, 2537.0], [1398816000000, 2603.0], [1401494400000, 2981.0], [1404086400000, 3325.0], [1406764800000, 4196.0], [1409443200000, 3350.0], [1412035200000, 3683.0], [1414713600000, 4661.0], [1417305600000, 3679.0], [1419984000000, 7318.0], [1422662400000, 3291.0], [1425081600000, 3551.0], [1427760000000, 3571.0], [1430352000000, 3573.0], [1433030400000, 3579.0], [1435622400000, 4145.0], [1438300800000, 4527.0], [1440979200000, 3473.0], [1443571200000, 4100.0], [1446249600000, 4220.0], [1448841600000, 3868.0], [1451520000000, 5392.0], [1454198400000, 2514.0], [1456704000000, 3545.0], [1459382400000, 3344.0], [1461974400000, 3543.0], [1464652800000, 3734.0], [1467244800000, 3915.0], [1469923200000, 4247.0], [1472601600000, 3903.0], [1475193600000, 4251.0], [1477872000000, 4309.0], [1480464000000, 4120.0], [1483142400000, 4355.0], [1485820800000, 2900.0], [1488240000000, 3407.0], [1490918400000, 3982.0]];
var na_hist_cached = {56500.0: 399, 234500.0: 1380, 224500.0: 1713, 308500.0: 277, 67500.0: 683, 63500.0: 336, 82500.0: 627, 166500.0: 419, 334500.0: 633, 212500.0: 267, 53500.0: 305, 138500.0: 309, 24500.0: 898, 489500.0: 214, 79500.0: 2923, 163500.0: 331, 574500.0: 190, 34500.0: 1139, 499500.0: 498, 50500.0: 316, 209500.0: 1771, 339500.0: 831, 105500.0: 511, 104500.0: 1603, 160500.0: 372, 152500.0: 508, 47500.0: 527, 131500.0: 526, 189500.0: 2168, 299500.0: 1763, 274500.0: 1231, 172500.0: 487, 73500.0: 339, 157500.0: 553, 241500.0: 244, 319500.0: 945, 409500.0: 551, 231500.0: 228, 15500.0: 186, 99500.0: 3437, 124500.0: 2373, 183500.0: 196, 38500.0: 307, 524500.0: 270, 273500.0: 228, 125500.0: 405, 23500.0: 215, 102500.0: 366, 180500.0: 351, 439500.0: 372, 429500.0: 399, 379500.0: 599, 235500.0: 227, 122500.0: 529, 206500.0: 265, 464500.0: 208, 374500.0: 641, 9500.0: 332, 93500.0: 288, 116500.0: 415, 176500.0: 538, 229500.0: 1943, 64500.0: 1823, 148500.0: 391, 484500.0: 288, 186500.0: 342, 123500.0: 485, 90500.0: 322, 129500.0: 2556, 143500.0: 286, 76500.0: 428, 61500.0: 575, 145500.0: 583, 292500.0: 203, 32500.0: 349, 649500.0: 280, 284500.0: 1034, 194500.0: 1803, 121500.0: 416, 255500.0: 287, 198500.0: 445, 58500.0: 327, 142500.0: 525, 78500.0: 327, 394500.0: 429, 113500.0: 250, 41500.0: 481, 281500.0: 302, 35500.0: 369, 84500.0: 1997, 168500.0: 316, 252500.0: 411, 120500.0: 316, 139500.0: 2633, 80500.0: 342, 26500.0: 267, 110500.0: 417, 141500.0: 474, 216500.0: 258, 81500.0: 535, 165500.0: 302, 249500.0: 2248, 162500.0: 633, 226500.0: 326, 52500.0: 514, 136500.0: 565, 220500.0: 469, 304500.0: 629, 247500.0: 324, 107500.0: 437, 191500.0: 343, 289500.0: 1095, 359500.0: 682, 268500.0: 297, 246500.0: 350, 414500.0: 350, 49500.0: 2584, 133500.0: 296, 217500.0: 406, 161500.0: 385, 469500.0: 292, 188500.0: 199, 272500.0: 258, 182500.0: 483, 519500.0: 238, 159500.0: 2578, 197500.0: 405, 46500.0: 452, 267500.0: 260, 214500.0: 1374, 17500.0: 186, 101500.0: 499, 185500.0: 434, 269500.0: 1244, 96500.0: 594, 108500.0: 229, 72500.0: 550, 204500.0: 1320, 324500.0: 824, 309500.0: 903, 43500.0: 285, 127500.0: 786, 211500.0: 502, 699500.0: 198, 14500.0: 344, 266500.0: 214, 147500.0: 665, 95500.0: 363, 27500.0: 344, 40500.0: 261, 244500.0: 1178, 179500.0: 2477, 154500.0: 1877, 140500.0: 575, 137500.0: 667, 37500.0: 514, 222500.0: 316, 92500.0: 618, 65500.0: 350, 344500.0: 518, 51500.0: 374, 119500.0: 2999, 264500.0: 1257, 118500.0: 421, 202500.0: 391, 286500.0: 277, 232500.0: 287, 173500.0: 240, 221500.0: 243, 509500.0: 202, 60500.0: 302, 144500.0: 1959, 193500.0: 431, 434500.0: 269, 31500.0: 305, 115500.0: 281, 399500.0: 822, 290500.0: 190, 454500.0: 202, 199500.0: 2898, 98500.0: 326, 170500.0: 264, 254500.0: 1039, 134500.0: 2122, 57500.0: 549, 156500.0: 422, 86500.0: 461, 196500.0: 294, 177500.0: 488, 83500.0: 434, 167500.0: 733, 251500.0: 476, 87500.0: 592, 419500.0: 448, 70500.0: 455, 54500.0: 1458, 29500.0: 1339, 474500.0: 342, 109500.0: 2350, 219500.0: 2094, 277500.0: 325, 529500.0: 209, 69500.0: 2476, 44500.0: 1506, 112500.0: 423, 151500.0: 522, 354500.0: 426, 135500.0: 378, 164500.0: 2037, 261500.0: 228, 22500.0: 245, 106500.0: 386, 190500.0: 368, 225500.0: 203, 77500.0: 603, 218500.0: 192, 245500.0: 220, 329500.0: 856, 75500.0: 452, 749500.0: 211, 111500.0: 467, 384500.0: 447, 19500.0: 721, 103500.0: 295, 187500.0: 481, 271500.0: 188, 236500.0: 280, 132500.0: 997, 33500.0: 257, 74500.0: 2309, 158500.0: 479, 242500.0: 460, 114500.0: 1907, 45500.0: 469, 153500.0: 275, 213500.0: 234, 549500.0: 356, 100500.0: 236, 184500.0: 1703, 174500.0: 2006, 155500.0: 381, 71500.0: 543, 89500.0: 2558, 239500.0: 1695, 195500.0: 237, 42500.0: 491, 126500.0: 489, 294500.0: 946, 97500.0: 496, 181500.0: 347, 349500.0: 1173, 128500.0: 302, 68500.0: 349, 55500.0: 331, 237500.0: 508, 404500.0: 305, 39500.0: 1860, 207500.0: 554, 66500.0: 531, 459500.0: 297, 94500.0: 1813, 178500.0: 262, 262500.0: 270, 279500.0: 1289, 233500.0: 250, 317500.0: 247, 257500.0: 283, 130500.0: 315, 36500.0: 340, 364500.0: 481, 288500.0: 222, 599500.0: 301, 7500.0: 230, 91500.0: 564, 175500.0: 365, 259500.0: 1590, 449500.0: 631, 48500.0: 334, 62500.0: 612, 146500.0: 472, 314500.0: 682, 150500.0: 287, 117500.0: 621, 201500.0: 248, 369500.0: 563, 149500.0: 3698, 494500.0: 208, 88500.0: 491, 171500.0: 589, 256500.0: 202, 424500.0: 418, 59500.0: 2390, 227500.0: 322, 192500.0: 425, 479500.0: 265, 30500.0: 260, 444500.0: 263, 389500.0: 479, 21500.0: 196, 85500.0: 391, 169500.0: 2335, 215500.0: 333};