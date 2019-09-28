<template>
  <div>
    <mu-option key="intro_index" label="首页声明" value="/"></mu-option>
    <mu-option key="intro_mode" label="赛事与赛制" value="intro_icpc"></mu-option>
    <mu-option key="intro_resource" label="学习资源" value="intro_resources"></mu-option>
    <mu-option key="intro_mistake" label="常见错误" value="intro_common-mistakes"></mu-option>
    <mu-option key="intro_trick" label="常见技巧" value="intro_common-tricks"></mu-option>
    <mu-option key="intro_nontraditional" label="非传统题" value="intro_non-trad"></mu-option>
    <mu-option key="intro_about" label="关于OI Wiki" value="intro_about"></mu-option>
    <mu-option key="basic_index" label="基础简介" value="basic"></mu-option>
    <mu-option key="basic_enumerate" label="枚举" value="basic_enumerate"></mu-option>
    <mu-option key="basic_simulate" label="模拟" value="basic_simulate"></mu-option>
    <mu-option key="basic_divideandconquer" label="递归与分治" value="basic_divide-and-conquer"></mu-option>
    <mu-option key="basic_greedy" label="贪心" value="basic_greedy"></mu-option>
    <mu-option key="basic_sortintro" label="排序简介" value="basic_sort-intro"></mu-option>
    <mu-option key="basic_selectionsort" label="选择排序" value="basic_selection-sort"></mu-option>
    <mu-option key="basic_bubblesort" label="冒泡排序" value="basic_bubble-sort"></mu-option>
    <mu-option key="basic_insertion_sort" label="插入排序" value="basic_insertion-sort"></mu-option>
    <mu-option key="basic_bucketsort" label="计数排序" value="basic_counting-sort"></mu-option>
    <mu-option key="basic_quicksort" label="快速排序" value="basic_quick-sort"></mu-option>
    <mu-option key="basic_mergesort" label="归并排序" value="basic_merge-sort"></mu-option>
    <mu-option key="basic_heapsort" label="堆排序" value="basic_heap-sort"></mu-option>
    <mu-option key="basic_bucketsort" label="桶排序" value="basic_bucket-sort"></mu-option>
    <mu-option key="basic_radixsort" label="基数排序" value="basic_radix-sort"></mu-option>
    <mu-option key="basic_shellsort" label="希尔排序" value="basic_shell-sort"></mu-option>
    <mu-option key="basic_stlsort" label="排序相关 STL" value="basic_stl-sort"></mu-option>
    <mu-option key="basic_useofsort" label="排序应用" value="basic_use-of-sort"></mu-option>
    <mu-option key="basic_binary" label="二分与三分" value="basic_binary"></mu-option>
    <mu-option key="basic_binary-acc" label="倍增" value="basic_binary-acc"></mu-option>
    <mu-option key="basic_construction" label="构造" value="basic_construction"></mu-option>
    <mu-option key="basic_prefixsum" label="前缀和 & 差分" value="basic_prefix-sum"></mu-option>
    <mu-option key="dp_index" label="动态规划简介" value="dp"></mu-option>
    <mu-option key="dp_memo" label="记忆化搜索" value="dp_memo"></mu-option>
    <mu-option key="dp_knapsack" label="背包 DP" value="dp_knapsack"></mu-option>
    <mu-option key="dp_interval" label="区间 DP" value="dp_interval"></mu-option>
    <mu-option key="dp_dag" label="DAG 上的 DP" value="dp_dag"></mu-option>
    <mu-option key="dp_tree" label="树形 DP" value="dp_tree"></mu-option>
    <mu-option key="dp_state" label="状压 DP" value="dp_state"></mu-option>
    <mu-option key="dp_number" label="数位 DP" value="dp_number"></mu-option>
    <mu-option key="dp_plug" label="插头 DP" value="dp_plug"></mu-option>
    <mu-option key="dp_count" label="计数 DP" value="dp_count"></mu-option>
    <mu-option key="dp_binaryknapsack" label="二进制分组解多重背包" value="dp_binary-knapsack"></mu-option>
    <mu-option key="dp_monotonousqueuestack" label="单调队列/单调栈优化" value="dp_monotonous-queue-stack"></mu-option>
    <mu-option key="dp_convexhulloptimization" label="斜率优化" value="dp_opt_slope"></mu-option>
    <mu-option
      key="dp_knuthyaoquadrangleinequality"
      label="四边形不等式优化"
      value="dp_opt_quadrangle"
    ></mu-option>
    <mu-option key="dp_stateoptimization" label="状态设计优化" value="dp_opt_state"></mu-option>
    <mu-option key="dp_misc" label="其他 DP" value="dp_misc"></mu-option>

    <mu-option key="ds_index" label="数据结构简介" value="ds"></mu-option>

    <mu-option key="ds_stack" label="栈" value="ds_stack"></mu-option>
    <mu-option key="ds_queue" label="队列" value="ds_queue"></mu-option>
    <mu-option key="ds_linkedlist" label="链表" value="ds_linked-list"></mu-option>
    <mu-option key="ds_hash" label="哈希表" value="ds_hash"></mu-option>
    <mu-option key="ds_dsu" label="并查集" value="ds_dsu"></mu-option>
    <mu-option key="ds_heap" label="堆简介" value="ds_heap"></mu-option>
    <mu-option key="ds_binaryheap" label="二叉堆" value="ds_binary-heap"></mu-option>
    <mu-option key="ds_pairingheap" label="配对堆" value="ds_pairing-heap"></mu-option>
    <mu-option key="ds_leftist-tree" label="左偏树" value="ds_leftist-tree"></mu-option>
    <mu-option key="ds_squarerootdecomposition" label="分块思想" value="ds_decompose"></mu-option>
    <mu-option key="ds_blocklist" label="块状链表" value="ds_block-list"></mu-option>
    <mu-option key="ds_blockarray" label="块状数组" value="ds_block-array"></mu-option>
    <mu-option key="ds_treedecompose" label="树分块" value="ds_tree-decompose"></mu-option>
    <mu-option key="ds_sqrt-tree" label="SqrtTree" value="ds_sqrt-tree"></mu-option>
    <mu-option key="ds_monotonousstack" label="单调栈" value="ds_monotonous-stack"></mu-option>
    <mu-option key="ds_monotonousqueue" label="单调队列" value="ds_monotonous-queue"></mu-option>
    <mu-option key="ds_sparsetable" label="倍增" value="ds_sparse-table"></mu-option>
    <mu-option key="ds_bit" label="树状数组" value="ds_bit"></mu-option>
    <mu-option key="ds_segment" label="线段树" value="ds_seg"></mu-option>
    <mu-option key="ds_seg-beats" label="线段树区间历史最值" value="ds_seg-beats"></mu-option>
    <mu-option key="ds_dividing" label="划分树" value="ds_dividing"></mu-option>
    <mu-option key="ds_bst" label="二叉搜索树简介" value="ds_bst"></mu-option>
    <mu-option key="ds_treap" label="Treap" value="ds_treap"></mu-option>
    <mu-option key="ds_splay" label="Splay" value="ds_splay"></mu-option>
    <mu-option key="ds_wblt" label="WBLT" value="ds_wblt"></mu-option>
    <mu-option key="ds_sbt" label="Size Balanced Tree" value="ds_sbt"></mu-option>
    <mu-option key="ds_avl" label="AVL 树" value="ds_avl"></mu-option>
    <mu-option key="ds_scapegoat" label="替罪羊树" value="ds_sgt"></mu-option>
    <mu-option key="ds_scapegoat" label="笛卡尔树" value="ds_cartesian-tree"></mu-option>

    <mu-option key="ds_seginseg" label="线段树套线段树" value="ds_seg-in-seg"></mu-option>
    <mu-option key="ds_seginbalanced" label="平衡树套线段树" value="ds_seg-in-balanced"></mu-option>
    <mu-option key="ds_balancedinseg" label="线段树套平衡树" value="ds_balanced-in-seg"></mu-option>
    <mu-option key="ds_persistentinbit" label="树状数组套主席树" value="ds_persistent-in-bit"></mu-option>

    <mu-option key="ds_persistent" label="可持久化数据结构简介" value="ds_persistent"></mu-option>
    <mu-option key="ds_persistentseg" label="可持久化线段树" value="ds_persistent-seg"></mu-option>
    <mu-option key="ds_persistentblockarray" label="可持久化块状数组" value="ds_persistent-block-array"></mu-option>
    <mu-option key="ds_persistentbalanced" label="可持久化平衡树" value="ds_persistent-balanced"></mu-option>
    <mu-option key="ds_persistenttrie" label="可持久化字典树" value="ds_persistent-trie"></mu-option>
    <mu-option key="ds_persistent-heap" label="可持久化可并堆" value="ds_persistent-heap"></mu-option>
    <mu-option key="ds_kdt-heap" label="K-D Tree" value="ds_kdt"></mu-option>
    <mu-option key="ds_odt" label="珂朵莉树" value="ds_odt"></mu-option>
    <mu-option key="ds_lct" label="Link Cut Tree" value="ds_lct"></mu-option>
    <mu-option key="ds_ett" label="Euler Tour Tree" value="ds_ett"></mu-option>
    <mu-option key="ds_top-tree" label="Top Tree" value="ds_top-tree"></mu-option>
    <mu-option key="ds_divide-combine" label="析合树" value="ds_divide-combine"></mu-option>

    <mu-option key="geometry_index" label="计算几何简介" value="geometry"></mu-option>
    <mu-option key="geometry_2d" label="二维计算几何基础" value="geometry_2d"></mu-option>
    <mu-option key="geometry_3d" label="三维计算几何基础" value="geometry_3d"></mu-option>
    <mu-option key="geometry_distance" label="距离" value="geometry_distance"></mu-option>
    <mu-option key="geometry_pick" label="Pick 定理" value="geometry_pick"></mu-option>
    <mu-option key="geometry_triangulation" label="三角剖分" value="geometry_triangulation"></mu-option>
    <mu-option key="geometry_convexhull" label="凸包" value="geometry_convex-hull"></mu-option>
    <mu-option key="geometry_scanning" label="扫描线" value="geometry_scanning"></mu-option>
    <mu-option key="geometry_rotatingcalipers" label="旋转卡壳" value="geometry_rotating-calipers"></mu-option>
    <mu-option
      key="geometry_half-plane"
      label="半平面交"
      value="geometry_half-plane"
    ></mu-option>
    <mu-option key="geometry_nearestpoints" label="平面最近点对" value="geometry_nearest-points"></mu-option>
    <mu-option key="geometry_random-incremental" label="随机增量法" value="geometry_random-incremental"></mu-option>
    <mu-option key="geometry_magic" label="计算几何杂项" value="geometry_misc"></mu-option>

    <mu-option key="graph_index" label="图论简介" value="graph"></mu-option>
    <mu-option key="graph_basic" label="图论基础" value="graph_basic"></mu-option>
    <mu-option key="graph_dfs" label="图的遍历DFS" value="graph_dfs"></mu-option>
    <mu-option key="graph_bfs" label="图的遍历BFS" value="graph_bfs"></mu-option>
    <mu-option key="graph_treebasic" label="树基础" value="graph_tre-ebasic"></mu-option>
    <mu-option key="graph_lca" label="最近公共祖先" value="graph_lca"></mu-option>
    <mu-option key="graph_treemisc" label="树重心" value="graph_tree-misc"></mu-option>
    <mu-option key="graph_treehash" label="树哈希" value="graph_tree-hash"></mu-option>
    <mu-option
      key="graph_hld"
      label="树链剖分"
      value="graph_hld"
    ></mu-option>
    <mu-option key="graph_treedivide" label="树分治" value="graph_tree-divide"></mu-option>
    <mu-option key="graph_dynamictreedivide" label="动态树分治" value="graph_dynamic-tree-divide"></mu-option>
    <mu-option key="graph_virtualtree" label="虚树" value="graph_virtual-tree"></mu-option>
    <mu-option key="graph_dsuontree" label="树上启发式合并" value="graph_dsu-on-tree"></mu-option>
    <mu-option key="graph_matrixtree" label="矩阵树定理" value="graph_matrix-tree"></mu-option>
    <mu-option key="graph_dag" label="有向无环图" value="graph_dag"></mu-option>
    <mu-option key="graph_topo" label="拓扑排序" value="graph_topo"></mu-option>
    <mu-option key="graph_mst" label="最小生成树" value="graph_mst"></mu-option>
    <mu-option key="graph_mdst" label="最小树形图" value="graph_mdst"></mu-option>
    <mu-option key="graph_shortestpath" label="最短路" value="graph_shortest-path"></mu-option>
    <mu-option
      key="graph_diff-constraints"
      label="差分约束"
      value="graph_diff-constraints"
    ></mu-option>
    <mu-option key="graph_kthpath" label="K 短路" value="graph_kth-path"></mu-option>
    <mu-option key="graph_scc" label="强连通分量" value="graph_scc"></mu-option>
    <mu-option key="graph_bcc" label="双连通分量" value="graph_bcc"></mu-option>
    <mu-option key="graph_bridge" label="割点和桥" value="graph_bridge"></mu-option>
    <mu-option key="graph_2sat" label="2-SAT" value="graph_2-sat"></mu-option>
    <mu-option key="graph_euler" label="欧拉图" value="graph_euler"></mu-option>
    <mu-option key="graph_hamilton" label="哈密顿图" value="graph_hamilton"></mu-option>
    <mu-option key="graph_bigraph" label="二分图" value="graph_bi-graph"></mu-option>
    <mu-option key="graph_mincircle" label="最小环" value="graph_min-circle"></mu-option>
    <mu-option key="graph_planar" label="平面图" value="graph_planar"></mu-option>
    <mu-option key="graph_color" label="图的着色" value="graph_color"></mu-option>
    <mu-option key="graph_flow" label="网络流简介" value="graph_flow"></mu-option>
    <mu-option key="graph_maxflow" label="最大流" value="graph_flow_max-flow"></mu-option>
    <mu-option key="graph_flownode" label="拆点" value="graph_flow_node"></mu-option>
    <mu-option key="graph_mincut" label="最小割" value="graph_flow_min-cut"></mu-option>
    <mu-option key="graph_mincost" label="费用流" value="graph_flow_min-cost"></mu-option>
    <mu-option key="graph_flowbound" label="上下界网络流" value="graph_flow_bound"></mu-option>
    <mu-option key="graph_prufer" label="Prufer序列" value="graph_prufer"></mu-option>
    <mu-option key="graph_misc" label="图论杂项" value="graph_misc"></mu-option>

    <mu-option key="math_index" label="数学简介" value="math"></mu-option>
    <mu-option key="math_vector" label="向量" value="math_vector"></mu-option>
    <mu-option key="math_complex" label="复数" value="math_complex"></mu-option>
    <mu-option key="math_polar-coordinate" label="极坐标系" value="math_polar-coordinate"></mu-option>
    <mu-option key="math_bit" label="位运算" value="math_bit"></mu-option>
    <mu-option key="math_quickpow" label="快速幂" value="math_quick-pow"></mu-option>

    <mu-option key="math_prime" label="素数" value="math_prime"></mu-option>
    <mu-option key="math_gcd" label="最大公约数" value="math_gcd"></mu-option>
    <mu-option key="math_euler" label="欧拉函数" value="math_euler"></mu-option>
    <mu-option key="math_sieve" label="筛法" value="math_sieve"></mu-option>
    <mu-option key="math_fermat" label="欧拉定理和费马小定理" value="math_fermat"></mu-option>
    <mu-option key="math_euclidean" label="类欧几里得算法" value="math_euclidean"></mu-option>

    <mu-option key="math_bezouts" label="裴蜀定理" value="math_bezouts"></mu-option>
    <mu-option key="math_inverse" label="乘法逆元" value="math_inverse"></mu-option>
    <mu-option key="math_linearequation" label="线性同余方程" value="math_linear-equation"></mu-option>
    <mu-option key="math_crt" label="中国剩余定理" value="math_crt"></mu-option>
    <mu-option key="math_bsgs" label="BSGS" value="math_bsgs"></mu-option>
    <mu-option key="math_primitiveroot" label="原根" value="math_primitive-root"></mu-option>
    <mu-option key="math_lucas" label="卢卡斯定理" value="math_lucas"></mu-option>
    <mu-option key="math_base" label="进位制" value="math_base"></mu-option>
    <mu-option key="math_mobius" label="莫比乌斯反演" value="math_mobius"></mu-option>
    <mu-option key="math_du" label="杜教筛" value="math_du"></mu-option>
    <mu-option key="math_min-25" label="Min_25筛" value="math_min-25"></mu-option>

    <mu-option key="math_matrix" label="矩阵" value="math_matrix"></mu-option>
    <mu-option key="math_gauss" label="高斯消元" value="math_gauss"></mu-option>
    <mu-option key="math_basis" label="线性基" value="math_basis"></mu-option>
    
    <mu-option key="math_polyintro" label="多项式部分简介" value="math_poly_intro"></mu-option>
    <mu-option key="math_lagrangepoly" label="拉格朗日插值" value="math_poly_lagrange"></mu-option>
    <mu-option key="math_fft" label="快速傅里叶变换" value="math_fft"></mu-option>
    <mu-option key="math_ntt" label="快速数论变换" value="math_ntt"></mu-option>
    <mu-option key="math_fwt" label="快速沃尔什变换" value="math_fwt"></mu-option>
    <mu-option key="math_sqrt" label="多项式开方" value="math_sqrt"></mu-option>
    <mu-option key="math_inv" label="多项式求逆" value="math_inv"></mu-option>
    <mu-option key="math_divmod" label="多项式除法|取模" value="math_div-mod"></mu-option>
    <mu-option key="math_lnexp" label="多项式对数函数|指数函数" value="math_ln-exp"></mu-option>
    <mu-option key="math_newton" label="多项式牛顿迭代" value="math_newton"></mu-option>
    <mu-option
      key="math_multipointevalinterpolation"
      label="多项式多点求值|快速插值"
      value="math_multipoint-eval-interpolation"
    ></mu-option>
    <mu-option key="math_trifunc" label="多项式三角函数" value="math_tri-func"></mu-option>
    <mu-option key="math_invtrifunc" label="多项式反三角函数" value="math_inv-tri-func"></mu-option>
    <mu-option key="math_combination" label="排列组合" value="math_combination"></mu-option>
    <mu-option key="math_catalan" label="卡特兰数" value="math_catalan"></mu-option>
    <mu-option key="math_stirling" label="斯特林数" value="math_stirling"></mu-option>
    <mu-option key="math_cantor" label="康托展开" value="math_cantor"></mu-option>
    <mu-option
      key="math_inclusionexclusionprinciple"
      label="容斥原理"
      value="math_inclusion-exclusion-principle"
    ></mu-option>
    <mu-option key="math_drawerprinciple" label="抽屉原理" value="math_drawer-principle"></mu-option>
    <mu-option key="math_expectation" label="概率和期望" value="math_expectation"></mu-option>
    <mu-option key="math_permutationgroup" label="置换群" value="math_permutation-group"></mu-option>
    <mu-option key="math_integral" label="数值积分" value="math_integral"></mu-option>
    <mu-option key="math_linearprogramming" label="线性规划" value="math_linear-programming"></mu-option>
    <mu-option key="math_simplex" label="单纯形法" value="math_simplex"></mu-option>
    <mu-option key="math_gametheory" label="博弈论" value="math_game-theory"></mu-option>

    <mu-option key="math_newton" label="牛顿迭代法" value="math_newton"></mu-option>
    <mu-option key="math_integral" label="数值积分" value="math_integral"></mu-option>
    <mu-option key="math_bignum" label="高精度算法" value="math_bignum"></mu-option>
    <mu-option key="math_dictionary" label="分段打表" value="math_dictionary"></mu-option>
    <mu-option key="math_fibonacci" label="斐波那契数列" value="math_fibonacci"></mu-option>

    <mu-option key="misc_index" label="杂项简介" value="misc"></mu-option>
    <mu-option key="misc_io" label="读入、输出优化" value="misc_io"></mu-option>
    <mu-option key="misc_complexity" label="复杂度" value="misc_complexity"></mu-option>
    <mu-option key="misc_discrete" label="离散化" value="misc_discrete"></mu-option>
    <mu-option key="misc_fractionalprogramming" label="分数规划" value="misc_frac-programming"></mu-option>
    <mu-option key="misc_offline" label="离线算法简介" value="misc_offline"></mu-option>
    <mu-option key="misc_cdqdivide" label="CDQ 分治" value="misc_cdq-divide"></mu-option>
    <mu-option key="misc_moalgo" label="莫队算法" value="misc_mo-algo"></mu-option>
    <mu-option key="misc_parallmu-binsearch" label="整体二分" value="misc_parallmu-binsearch"></mu-option>
    <mu-option key="misc_random" label="随机函数" value="misc_random"></mu-option>
    <mu-option key="misc_hillclimbing" label="爬山算法" value="misc_hill-climbing"></mu-option>
    <mu-option key="misc_simulatedannealing" label="模拟退火" value="misc_simulated-annealing"></mu-option>

    <mu-option key="misc_largestmatrix" label="悬线法" value="misc_largest-matrix"></mu-option>
    <mu-option key="misc_ccbasic" label="计算理论基础" value="misc_cc-basic"></mu-option>
    <mu-option key="misc_endianness" label="字节顺序" value="misc_endianness"></mu-option>
    <mu-option key="misc_josephus" label="约瑟夫环问题" value="misc_josephus"></mu-option>
    <mu-option key="misc_stern-brocot" label="Stern-Brocot 树与 Farey 序列" value="misc_stern-brocot"></mu-option>
    <mu-option key="misc_gray-code" label="格雷码" value="misc_gray-code"></mu-option>
<mu-option key="misc_expression" label="表达式求值" value="misc_expression"></mu-option>
<mu-option key="misc_job-order" label="在一台机器上规划任务" value="misc_job-order"></mu-option>


    <mu-option key="search_index" label="搜索简介" value="search"></mu-option>
    <mu-option key="search_dfs" label="DFS" value="search_dfs"></mu-option>
    <mu-option key="search_bfs" label="BFS" value="search_bfs"></mu-option>
    <mu-option key="search_bidirectional" label="双向搜索" value="search_bidirectional"></mu-option>
    <mu-option key="search_heuristic" label="启发式搜索" value="search_heuristic"></mu-option>
    <mu-option key="search_astar" label="A*" value="search_astar"></mu-option>
    <mu-option key="search_iterative" label="迭代加深搜索" value="search_iterative"></mu-option>
    <mu-option key="search_idastar" label="IDA*" value="search_idastar"></mu-option>
    <mu-option key="search_backtracking" label="回溯法" value="search_backtracking"></mu-option>
    <mu-option key="search_dlx" label="舞蹈链" value="search_dlx"></mu-option>
    <mu-option key="search_optimization" label="优化与剪枝" value="search_opt"></mu-option>
    <mu-option key="string_index" label="字符串简介" value="string"></mu-option>
    <mu-option key="string_libfunc" label="标准库函数" value="string_lib-func"></mu-option>
    <mu-option key="string_match" label="字符串匹配" value="string_match"></mu-option>
    <mu-option key="string_hash" label="哈希" value="string_hash"></mu-option>
    <mu-option key="string_prefixfunction" label="前缀函数与 KMP 算法" value="string_kmp"></mu-option>
    <mu-option key="string_trie" label="字典树 (Trie)" value="string_trie"></mu-option>
    <mu-option key="string_pam" label="回文自动机" value="string_pam"></mu-option>
    <mu-option key="string_sa" label="后缀数组 (SA)" value="string_sa"></mu-option>
    <mu-option key="string_acautomaton" label="AC 自动机" value="string_acautomaton"></mu-option>
    <mu-option key="string_sam" label="后缀自动机 (SAM)" value="string_sam"></mu-option>
    <mu-option key="string_suffixtree" label="后缀树" value="string_suffix-tree"></mu-option>
    <mu-option key="string_manacher" label="Manacher" value="string_manacher"></mu-option>
    <mu-option key="string_minimalstring" label="最小表示法" value="string_minimal-string"></mu-option>
    <mu-option key="string_zfunction" label="Z 函数（扩展 KMP）" value="string_z-func"></mu-option>
    <mu-option key="string_lyndon" label="Lyndon 分解" value="string_lyndon"></mu-option>
    <mu-option key="topic_rmq" label="RMQ" value="topic_rmq"></mu-option>
    <mu-option v-for="item in menulist" :key="item.type" :label="item.title" :value="item.type"></mu-option>
  </div>
</template>

<script>
export default {
  name: "algorithmselect",

  data() {
    return {
      value: "",
      searchtext: "",
      editpage: "",
      menulist: []
    };
  },
  created() {
    this.$axios
      .get("/wiki/?std=1")
      .then(response => {
        this.menulist = response.data;
      })
      .catch(error => {
        this.$toast.error(
          "服务器错误！" + "(" + JSON.stringify(error.response.data) + ")"
        );
      });
  },
  methods: {}
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
