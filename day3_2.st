| wire1 wire2 move checkCross minDistance |

wire1 := 'R1009,D335,L942,D733,L398,U204,L521,D347,L720,U586,R708,D746,L292,U416,L824,U20,R359,D828,R716,U895,L498,D671,L325,D68,L667,U134,L435,D44,R801,U654,R188,U542,L785,D318,L806,U602,L465,U239,R21,U571,R653,U436,L52,U380,R446,D960,R598,U590,L47,U972,L565,D281,R790,U493,R864,D396,R652,D775,L939,D284,R554,U629,L842,D837,R554,D795,R880,D301,R948,U974,L10,D898,R588,D743,L334,U59,L413,U511,L132,U771,R628,D805,R465,D561,R18,D169,L580,D99,L508,U964,L870,D230,L472,U897,L85,U306,L103,U322,L637,U464,R129,D514,R454,U479,R801,U18,R929,U181,L113,D770,L173,D124,L122,U481,L666,D942,L534,U608,R90,U576,L641,U249,L857,U197,R783,D92,L938,D192,L698,D862,R995,U12,R766,D323,R934,U315,R956,D234,R983,D246,L153,U26,L779,D628,R174,D385,L758,D486,R132,U414,R915,D511,L152,D309,L708,D755,L679,D166,L699,U734,R55,D224,L582,U798,L348,U219,L304,U621,L788,D538,R781,D509,R486,U581,R759,D892,R16,D552,L82,D618,L309,D610,L645,U146,L328,U569,L307,D385,L249,D231,R928,U681,R384,D337,R715,D798,L788,D604,R517,U766,R368,U430,L49,U236,R621,U656,R997,U268,L18,D789,L935,D87,L670,U35,R463,D71,R268,U728,R693,D863,R656,D654,L350,U796,L72,U562,R56,U10,L651,D751,L557,D518,R901,D741,R787,D332,R723,D980,R206,U670,R645,D927,L641,D863,R478,D568,L858,D990,L124,D864,L162,U361,L407,U674,R508,D284,L675,D794,L138,U55,L781,U37,R956,D364,L111,U721,L91,U559,L852,U351,R994,U446,L162,D345,R92,D941,R572,U185,R615,D590,R459,D313,R127,D315,R96,U751,R210,D620,L790,U826,R410,D652,R549,D698,L805,U814,L364,U905,L96,U997,L689' splitString: ','.
wire2 := 'L1008,D451,L146,D628,R877,U486,L464,U815,L119,U208,R686,U477,L510,D353,R189,D437,R461,D645,R639,U650,R491,D744,L798,U514,R598,U64,R668,U771,R21,U782,L564,U632,R23,U112,R947,U649,L205,D804,R277,U683,L828,U662,R890,U420,L908,U484,R535,D515,R390,U7,L287,D967,R497,U502,L893,D851,R426,D656,R622,U46,L106,U590,R646,D29,R467,D896,L155,U382,L992,D189,L34,U16,R132,U35,L586,U812,L539,D409,R776,D42,R58,U323,R569,D965,R648,D789,R478,D587,R162,D834,R979,D993,L944,U84,R93,U903,R491,U713,L646,U235,R120,U286,L919,U34,L662,U834,L812,D271,L73,U410,L758,U210,R712,U581,L520,D654,L981,D516,R312,U123,L153,U433,R368,U606,L882,U362,L261,U587,R441,D691,L699,U135,L825,D25,R142,U191,L358,D554,L487,D802,L542,D266,R283,U222,R113,D259,R828,U182,R402,U627,R769,D426,L768,U571,R118,U684,R803,D430,R942,U514,R711,D225,R299,U45,L214,U712,L673,U787,L164,D703,L616,D587,R624,D326,L614,D779,L904,D563,L98,U137,R687,U425,R615,U671,L361,D47,L767,D951,R791,D116,R664,U704,R291,U535,L322,D989,R467,U7,L974,D276,R901,U51,L567,D641,R112,U102,R753,D127,R486,D143,R259,U212,L97,U505,R377,U473,R514,D912,L928,U401,R772,D416,R695,U784,L524,D341,R402,U749,L1,U1,L109,U921,L754,U66,L927,U708,R551,D687,R129,D346,L408,D330,L300,D920,R170,D353,R97,D74,R850,D511,R275,U872,L748,U344,R610,D391,R963,D98,L89,U259,R651,U651,L31,D142,L104,U770,L482,D677,R823,D110,L606,U897,L631,U437,L551,D550,R301,D762,R349,D824,R260,U438,R249,D636,L386,U926,R367,U231,R752,U854,L481,D764,R516,D273,L726,D778,R483,U513,R129,D135,L224' splitString: ','.

minDistance := nil.

move := [:pos :instr |
	"i don't think this is idiomatic smalltalk"
	| dir num |
	dir := instr at: 1.
	num := (instr copyFrom: 2) asNumber.

	dir = $U ifTrue: [
		Point x: (pos x) y: (pos y + num)
	]
	ifFalse: [dir = $D ifTrue: [
		Point x: (pos x) y: (pos y - num)
	]
	ifFalse: [dir = $R ifTrue: [
		Point x: (pos x + num) y: (pos y)
	]
	ifFalse: [dir = $L ifTrue: [
		Point x: (pos x - num) y: (pos y)
	]]]].
].

checkCross := [:pos1a :pos1b :pos2a :pos2b |
	| x_tests y_tests |
	x_tests := Array
		with: (pos1a x <= pos2a x) & (pos2a x <= pos1b x)
		with: (pos1a x >= pos2a x) & (pos2a x >= pos1b x)
		with: (pos2a x <= pos1a x) & (pos1a x <= pos2b x)
		with: (pos2a x >= pos1a x) & (pos1a x >= pos2b x).

	y_tests := Array
		with: (pos1a y <= pos2a y) & (pos2a y <= pos1b y)
		with: (pos1a y >= pos2a y) & (pos2a y >= pos1b y)
		with: (pos2a y <= pos1a y) & (pos1a y <= pos2b y)
		with: (pos2a y >= pos1a y) & (pos1a y >= pos2b y).

	(x_tests includes: true) and: [
		y_tests includes: true
	]
].

[
	| wire1_pos wire1_totalsteps |
	wire1_pos := 0@0.
	wire1_totalsteps := 0.
	wire1 do: [:wire1_instr |
		| wire1_new_pos wire2_pos wire1_dir wire1_steps wire2_totalsteps |
		wire1_dir := wire1_instr at: 1.
		wire1_steps := (wire1_instr copyFrom: 2) asNumber.
		wire1_new_pos := move value: wire1_pos value: wire1_instr.

		wire2_pos := 0@0.
		wire2_totalsteps := 0.
		wire2 do: [:wire2_instr |
			| wire2_new_pos wire2_dir wire2_steps |
			wire2_dir := wire2_instr at: 1.
			wire2_steps := (wire2_instr copyFrom: 2) asNumber.
			wire2_new_pos := move value: wire2_pos value: wire2_instr.

			"detect whether the line from wire1_pos to wire1_new_pos
			and the line from wire2_pos to wire2_new_pos
			cross each other"
			(checkCross
				value: wire1_pos
				value: wire1_new_pos
				value: wire2_pos
				value: wire2_new_pos)
			ifTrue: [
				"find things"
				| wire1_positions wire2_positions positions |
				wire1_dir = $U ifTrue: [wire1_positions := ((wire1_pos y) to: (wire1_new_pos y))
															collect: [:y | Point x: (wire1_pos x) y: y]].
				wire1_dir = $D ifTrue: [wire1_positions := ((wire1_new_pos y) to: (wire1_pos y))
															collect: [:y | Point x: (wire1_pos x) y: y]].
				wire1_dir = $R ifTrue: [wire1_positions := ((wire1_pos x) to: (wire1_new_pos x))
															collect: [:x | Point x: x y: (wire1_pos y)]].
				wire1_dir = $L ifTrue: [wire1_positions := ((wire1_new_pos x) to: (wire1_pos x))
															collect: [:x | Point x: x y: (wire1_pos y)]].

				wire2_dir = $U ifTrue: [wire2_positions := ((wire2_pos y) to: (wire2_new_pos y))
															collect: [:y | Point x: (wire2_pos x) y: y]].
				wire2_dir = $D ifTrue: [wire2_positions := ((wire2_new_pos y) to: (wire2_pos y))
															collect: [:y | Point x: (wire2_pos x) y: y]].
				wire2_dir = $R ifTrue: [wire2_positions := ((wire2_pos x) to: (wire2_new_pos x))
															collect: [:x | Point x: x y: (wire2_pos y)]].
				wire2_dir = $L ifTrue: [wire2_positions := ((wire2_new_pos x) to: (wire2_pos x))
															collect: [:x | Point x: x y: (wire2_pos y)]].

				positions := wire1_positions select: [:each | wire2_positions includes: each].
				
				positions do: [:pos |
					pos = (0@0) ifFalse: [
						| total wire1_totalsteps2 wire2_totalsteps2 |
						wire1_totalsteps2 := wire1_totalsteps + (pos x - wire1_pos x) abs
															 + (pos y - wire1_pos y) abs.
						wire2_totalsteps2 := wire2_totalsteps + (pos x - wire2_pos x) abs
															 + (pos y - wire2_pos y) abs.
						total := wire1_totalsteps2 + wire2_totalsteps2.
						minDistance isNil ifTrue: [minDistance := total]
							ifFalse: [
								total < minDistance ifTrue: [minDistance := total]
							].
					]
				]
			].

			wire2_pos := wire2_new_pos.
			wire2_totalsteps := wire2_totalsteps + wire2_steps.
		].
		wire1_pos := wire1_new_pos.
		wire1_totalsteps := wire1_totalsteps + wire1_steps.
	].
] value.

^minDistance