import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 添加五年级和六年级母题数据
# 找到 allTopics 定义位置并添加新年级

grade5_math = '''
// 五年级数学21道
const topicsMath5 = [
    {id:101,title:'小数加减法',diff:2,q:'计算：3.25+1.75=',a:'5',e:'对齐小数点相加'},
    {id:102,title:'小数乘法',diff:2,q:'计算：0.5×0.4=',a:'0.2',e:'按整数乘法计算后点小数点'},
    {id:103,title:'小数除法',diff:3,q:'计算：4.8÷0.6=',a:'8',e:'被除数和除数同时扩大10倍'},
    {id:104,title:'面积计算',diff:2,q:'长方形长5cm，宽3cm，面积是？',a:'15cm²',e:'面积=长×宽'},
    {id:105,title:'三角形面积',diff:3,q:'底8cm，高5cm的三角形面积是？',a:'20cm²',e:'面积=底×高÷2'},
    {id:106,title:'平行四边形面积',diff:3,q:'底6cm，高4cm，平行四边形面积是？',a:'24cm²',e:'面积=底×高'},
    {id:107,title:'分数意义',diff:2,q:'把一个蛋糕平均分成5份，取2份，用分数表示？',a:'2/5',e:'分子表示取的份数'},
    {id:108,title:'分数加减法',diff:3,q:'计算：1/3+1/6=',a:'1/2',e:'通分后相加'},
    {id:109,title:'公倍数',diff:3,q:'4和6的最小公倍数是？',a:'12',e:'列举法或短除法'},
    {id:110,title:'公因数',diff:3,q:'12和18的最大公因数是？',a:'6',e:'列举法或短除法'},
    {id:111,title:'方程初步',diff:2,q:'解方程：x+3=10',a:'x=7',e:'移项得x=10-3'},
    {id:112,title:'列方程解应用',diff:3,q:'小明有x本书，小红有15本，两人共25本，求x',a:'x=10',e:'x+15=25'},
    {id:113,title:'可能性',diff:2,q:'盒中有3红2白球，摸到红球的可能性是？',a:'3/5',e:'摸到红球次数/总次数'},
    {id:114,title:'统计图表',diff:2,q:'平均数怎么求？',a:'总数÷个数',e:'平均数=总和÷数量'},
    {id:115,title:'角的度量',diff:2,q:'直角是多少度？',a:'90°',e:'直角等于90度'},
    {id:116,title:'多边形内角和',diff:3,q:'五边形的内角和是？',a:'540°',e:'(5-2)×180°'},
    {id:117,title:'植树问题',diff:4,q:'在100米路两旁种树，每隔10米一棵，共几棵？',a:'22棵',e:'两端都种：棵数=段数+1'},
    {id:118,title:'周期问题',diff:3,q:'1,2,3循环排列，第10个是？',a:'1',e:'10÷3=3余1'},
    {id:119,title:'简便运算',diff:3,q:'125×8×4=',a:'4000',e:'125×8=1000'},
    {id:120,title:'体积计算',diff:3,q:'长方体长4cm，宽3cm，高2cm，体积是？',a:'24cm³',e:'体积=长×宽×高'},
    {id:121,title:'单位换算',diff:2,q:'2.5小时=多少分钟？',a:'150分钟',e:'2.5×60=150'}
];

// 五年级英语21道
const topicsEnglish5 = [
    {id:201,title:'一般现在时',diff:2,q:'She ____ (have) a cat.',a:'has',e:'第三人称单数动词加s/es'},
    {id:202,title:'现在进行时',diff:2,q:'He ____ (read) a book now.',a:'is reading',e:'be+动词ing'},
    {id:203,title:'情态动词',diff:2,q:'I ____ swim in the river.',a:'can',e:'can表示能力'},
    {id:204,title:'方位介词',diff:2,q:'The book is ____ the table.',a:'on',e:'on表示在...上面'},
    {id:205,title:'there be句型',diff:2,q:'____ a beautiful flower in the garden.',a:'There is',e:'就近原则'},
    {id:206,title:'特殊疑问句',diff:2,q:'____ is your name?',a:'What',e:'what问姓名'},
    {id:207,title:'形容词比较级',diff:2,q:'Tom is ____ (tall) than Jim.',a:'taller',e:'比较级加er'},
    {id:208,title:'一般过去时',diff:2,q:'Yesterday, I ____ (go) to school.',a:'went',e:'过去式不规则变化'},
    {id:209,title:'时间表达',diff:1,q:'7:15用英语怎么说？',a:'Seven fifteen / Quarter past seven',e:'时间表达方式'},
    {id:210,title:'可数不可数',diff:2,q:'____ (water) is important.',a:'Water',e:'水是不可数名词'},
    {id:211,title:'some/any',diff:2,q:'Are there ____ apples on the table?',a:'any',e:'否定疑问用any'},
    {id:212,title:'祈使句',diff:2,q:'____ (not run) in the hallway!',a:\"Don't run\",e:'否定祈使句用Don\\'t'},
    {id:213,title:'人称代词',diff:1,q:'This is ____ (I) book.',a:'my',e:'物主代词修饰名词'},
    {id:214,title:'like doing',diff:2,q:'I like ____ (swim).',a:'swimming',e:'like+动词ing'},
    {id:215,title:'选择疑问句',diff:2,q:'Is it red ____ blue?',a:'or',e:'or表示选择'},
    {id:216,title:'频率副词',diff:2,q:'He ____ (always/often) comes late.',a:'often',e:'频率副词位置'},
    {id:217,title:'现在进行时构成',diff:2,q:'____ (be) you listening?',a:'Are',e:'be+主语+动词ing'},
    {id:218,title:'名词复数',diff:2,q:'There are five ____ (child) in the room.',a:'children',e:'child的复数是children'},
    {id:219,title:'whose句型',diff:2,q:'____ coat is this?',a:'Whose',e:'whose问所属'},
    {id:220,title:'情态动词can',diff:2,q:'____ you speak English?',a:'Can',e:'can的一般疑问句'},
    {id:221,title:'词汇运用',diff:2,q:'Monday, Tuesday, ____ (Wednesday)',a:'Wednesday',e:'一周顺序'}
];

// 五年级语文21道
const topicsChinese5 = [
    {id:301,title:'拼音拼读',diff:1,q:'\"骄傲\"的读音是？',a:'jiāo ào',e:'骄傲是多音字'},
    {id:302,title:'字形辨析',diff:2,q:'下列词语中没有错别字的是：A决不相同 B绝不相同 C决不不相同 D绝不相同',a:'B',e:'\"决\"和\"绝\"区别'},
    {id:303,title:'词语搭配',diff:2,q:'依次填入：同学们正在____地讨论问题。',a:'热烈',e:'讨论搭配热烈'},
    {id:304,title:'标点符号',diff:2,q:'\"今天天气真好呀！\"这句话用了什么标点？',a:'感叹号',e:'表示强烈感情'},
    {id:305,title:'句子排序',diff:3,q:'将句子重新排序：①于是②他③跑④很快⑤因为⑥迟到',a:'⑤①②③④',e:'因为...于是...'},
    {id:306,title:'修辞手法',diff:2,q:'\"星星像眼睛\"用了什么修辞？',a:'比喻',e:'把星星比作眼睛'},
    {id:307,title:'古诗默写',diff:2,q:'默写《悯农》前两句',a:'锄禾日当午，汗滴禾下土',e:'李绅名篇'},
    {id:308,title:'古诗理解',diff:2,q:'《静夜思》作者是谁？',a:'李白',e:'唐代诗人'},
    {id:309,title:'阅读理解',diff:3,q:'概括段落主要内容的方法是什么？',a:'找关键句或归纳要点',e:'段落大意概括'},
    {id:310,title:'近义词辨析',diff:2,q:'\"安静\"和\"宁静\"有什么区别？',a:'宁静程度更深',e:'近义词细微差别'},
    {id:311,title:'反义词',diff:1,q:'\"高大\"的反义词是？',a:'矮小',e:'反义词配对'},
    {id:312,title:'词语分类',diff:2,q:'\"苹果、香蕉、椅子、葡萄\"中不同类的是？',a:'椅子',e:'水果vs家具'},
    {id:313,title:'句式转换',diff:2,q:'把\"我完成了作业。\"改成感叹句',a:'我终于完成了作业！',e:'添加感叹词'},
    {id:314,title:'病句修改',diff:3,q:'修改：春天来了，花园里开满了五颜六色的红花。',a:'春天来了，花园里开满了五颜六色的花。',e:'五颜六色和红花矛盾'},
    {id:315,title:'缩写句子',diff:2,q:'缩写：我和爸爸一起去公园散步。',a:'我和爸爸散步。',e:'保留主谓宾'},
    {id:316,title:'扩写句子',diff:2,q:'扩写：小鸟唱歌。',a:'可爱的小鸟在枝头欢快地唱歌。',e:'添加修饰语'},
    {id:317,title:'查字典',diff:2,q:'\"凹\"字用部首查字法，先查什么部？',a:'凵',e:'凹的部首是凵'},
    {id:318,title:'语言表达',diff:2,q:'如何用礼貌用语向别人借书？',a:'请问可以借你的书吗？',e:'使用请、好吗等'},
    {id:319,title:'口语交际',diff:2,q:'当别人帮助了你，你该怎么说？',a:'谢谢你！',e:'表达感谢'},
    {id:320,title:'写作要素',diff:2,q:'记叙文的六要素是什么？',a:'时间、地点、人物、起因、经过、结果',e:'记叙文要素'},
    {id:321,title:'名著阅读',diff:2,q:'《西游记》中孙悟空使用的兵器叫什么？',a:'如意金箍棒',e:'东海龙宫的定海神针'}
];'''

grade6_math = '''
// 六年级数学21道
const topicsMath6 = [
    {id:101,title:'分数乘法',diff:2,q:'计算：2/3×6=',a:'4',e:'分子分母约分'},
    {id:102,title:'分数除法',diff:3,q:'计算：3/4÷2=',a:'3/8',e:'除以一个数等于乘倒数'},
    {id:103,title:'比的意义',diff:2,q:'3:5的比值是？',a:'3/5或0.6',e:'比值=前项÷后项'},
    {id:104,title:'比的化简',diff:2,q:'化简：12:18',a:'2:3',e:'除以最大公约数'},
    {id:105,title:'百分数应用',diff:3,q:'50的20%是多少？',a:'10',e:'50×20%=10'},
    {id:106,title:'圆的认识',diff:2,q:'圆的直径和半径关系是？',a:'d=2r',e:'直径是半径的2倍'},
    {id:107,title:'圆周率',diff:1,q:'圆周率π约等于？',a:'3.14',e:'圆周率定义'},
    {id:108,title:'圆的周长',diff:2,q:'半径2cm的圆，周长是？',a:'12.56cm',e:'C=2πr'},
    {id:109,title:'圆的面积',diff:3,q:'直径6cm的圆，面积是？',a:'28.26cm²',e:'S=πr²,r=3'},
    {id:110,title:'扇形面积',diff:3,q:'圆心角90°，半径4cm的扇形面积是？',a:'12.56cm²',e:'90/360×π×4²'},
    {id:111,title:'负数认识',diff:2,q:'-5℃比-2℃高还是低？',a:'低',e:'负数比较大小'},
    {id:112,title:'数轴表示',diff:2,q:'在数轴上，-3在-5的哪边？',a:'右边',e:'数轴上右边的数大'},
    {id:113,title:'解比例',diff:3,q:'解比例：3:x=6:8',a:'x=4',e:'内向积=外向积'},
    {id:114,title:'统计图选择',diff:2,q:'表示部分与整体关系用什么统计图？',a:'扇形统计图',e:'各部分占比'},
    {id:115,title:'圆柱体积',diff:3,q:'底面半径2cm，高5cm的圆柱体积是？',a:'62.8cm³',e:'V=πr²h'},
    {id:116,title:'圆锥体积',diff:3,q:'圆锥底面积12cm²，高9cm，体积是？',a:'36cm³',e:'V=1/3Sh'},
    {id:117,title:'比例尺',diff:3,q:'比例尺1:1000，表示实际1cm，图上？',a:'1m',e:'图上距离×1000'},
    {id:118,title:'正反比例',diff:3,q:'速度一定，路程和时间成什么比例？',a:'正比例',e:'s=vt'},
    {id:119,title:'应用题',diff:4,q:'一批零件，甲单独做8天完成，乙单独做12天，两人合作几天完成？',a:'4.8天',e:'合作效率=1/8+1/12'},
    {id:120,title:'利率问题',diff:3,q:'本金1000元，年利率3%，存一年利息？',a:'30元',e:'利息=本金×利率'},
    {id:121,title:'统计量',diff:2,q:'一组数据2,3,3,4,5,5,5的众数是？',a:'3和5',e:'出现次数最多的数'}
];

// 六年级英语21道
const topicsEnglish6 = [
    {id:201,title:'一般现在时',diff:2,q:'My mother ____ (work) in a hospital.',a:'works',e:'第三人称单数动词加s'},
    {id:202,title:'现在进行时',diff:2,q:'Look! The birds ____ (fly) in the sky.',a:'are flying',e:'现在进行时be+ing'},
    {id:203,title:'一般过去时',diff:2,q:'Last weekend, I ____ (visit) my grandparents.',a:'visited',e:'过去时间用过去式'},
    {id:204,title:'一般将来时',diff:2,q:'I ____ (go) to Beijing tomorrow.',a:'will go',e:'tomorrow用will'},
    {id:205,title:'现在完成时',diff:3,q:'I ____ (read) this book. It is very interesting.',a:'have read',e:'现在完成时强调结果'},
    {id:206,title:'情态动词must',diff:2,q:'You ____ (must) do your homework first.',a:'must',e:'must表示必须'},
    {id:207,title:'形容词比较级',diff:2,q:'The blue whale is the ____ (big) animal.',a:'biggest',e:'最高级前加the'},
    {id:208,title:'副词比较级',diff:2,q:'He runs ____ (fast) than me.',a:'faster',e:'副词比较级加er'},
    {id:209,title:'过去进行时',diff:3,q:'I ____ (read) when he called.',a:'was reading',e:'过去进行时was/were+ing'},
    {id:210,title:'there be将来时',diff:3,q:'There ____ (be) a concert tomorrow.',a:'will be / is going to be',e:'there be的一般将来时'},
    {id:211,title:'被动语态',diff:3,q:'The song ____ (sing) by millions of people.',a:'is sung',e:'一般现在时被动语态'},
    {id:212,title:'if条件句',diff:3,q:'If it ____ (rain), I will stay home.',a:'rains',e:'主将从现'},
    {id:213,title:'宾语从句',diff:3,q:'I think that he ____ (be) right.',a:'is',e:'宾语从句用陈述语序'},
    {id:214,title:'直接间接引语',diff:3,q:'She said, \"I am happy.\" 改为间接引语',a:'She said that she was happy.',e:'人称和时态变化'},
    {id:215,title:'used to',diff:3,q:'I ____ (use to) play with dolls.',a:'used to',e:'used to表示过去习惯'},
    {id:216,title:'动名词做主语',diff:2,q:'____ (read) is my hobby.',a:'Reading',e:'动名词可做主语'},
    {id:217,title:'短语动词',diff:2,q:'Please pick ____ the book.',a:'up',e:'pick up捡起'},
    {id:218,title:'介词辨析',diff:2,q:'We will meet ____ 7 o\\'clock ____ the morning.',a:'at / in',e:'at+时间点，in+早中晚'},
    {id:219,title:'复合形容词',diff:2,q:'a five-year-old boy 画线部分提问',a:'How old',e:'对年龄提问'},
    {id:220,title:'感叹句',diff:2,q:'改为感叹句：The flower is beautiful.',a:'How beautiful the flower is!',e:'How+adj+主谓'},
    {id:221,title:'阅读理解策略',diff:3,q:'阅读理解中，如何找主旨大意？',a:'看首段和末段',e:'阅读技巧'}
];

// 六年级语文21道
const topicsChinese6 = [
    {id:301,title:'拼音拼读',diff:1,q:'\"水平\"的读音是？',a:'shuǐ píng',e:'声调正确标注'},
    {id:302,title:'字形辨析',diff:2,q:'\"戊\"和\"戌\"的区别是？',a:'笔画不同',e:'戊wù戌xū'},
    {id:303,title:'词语搭配',diff:2,q:'依次填入：他_____地望着远方。',a:'凝视',e:'凝视表示专注地看'},
    {id:304,title:'成语运用',diff:2,q:'用\"专心致志\"造句',a:'同学们专心致志地听讲。',e:'形容精神集中'},
    {id:305,title:'病句修改',diff:3,q:'修改：通过讨论，使我们提高了认识。',a:'通过讨论，我们提高了认识。',e:'缺少主语'},
    {id:306,title:'修辞手法',diff:2,q:'\"月光如银\"用了什么修辞？',a:'比喻',e:'把月光比作银'},
    {id:307,title:'古诗理解',diff:3,q:'《春夜喜雨》中\"随风潜入夜\"的\"潜\"是什么意思？',a:'悄悄',e:'形容春雨细密无声'},
    {id:308,title:'古诗鉴赏',diff:3,q:'《望天门山》写了什么景物？',a:'天门山、楚江、帆船',e:'李白写景诗'},
    {id:309,title:'文言文翻译',diff:3,q:'翻译：学而时习之',a:'学了知识后按时复习',e:'《论语》名句'},
    {id:310,title:'文言虚词',diff:3,q:'\"之\"在\"学而时习之\"中的用法是？',a:'代词',e:'指代所学知识'},
    {id:311,title:'说明方法',diff:2,q:'\"这座塔高约50米\"用了什么说明方法？',a:'列数字',e:'用具体数字说明'},
    {id:312,title:'说明文语言',diff:3,q:'说明文语言有什么特点？',a:'准确性、严谨性',e:'科学性和真实性'},
    {id:313,title:'议论文要素',diff:2,q:'议论文的三要素是？',a:'论点、论据、论证',e:'议论文结构'},
    {id:314,title:'论证方法',diff:3,q:'举例说明\"勤奋出天才\"，用了什么论证方法？',a:'举例论证',e:'通过事例证明'},
    {id:315,title:'段落层次',diff:3,q:'划分段落层次的方法有哪些？',a:'按时间、空间、逻辑',e:'段落结构分析'},
    {id:316,title:'标题作用',diff:3,q:'分析《桥》这篇课文的标题作用',a:'象征、激发兴趣、线索',e:'标题的多重作用'},
    {id:317,title:'人物描写',diff:2,q:'\"他高高的个子\"用了什么描写方法？',a:'外貌描写',e:'对人物外形的描写'},
    {id:318,title:'环境描写',diff:2,q:'小说中开头描写恶劣天气有什么作用？',a:'渲染气氛、烘托心情',e:'环境描写作用'},
    {id:319,title:'写作手法',diff:3,q:'\"一切景语皆情语\"是什么意思？',a:'景物描写反映人物情感',e:'情景交融'},
    {id:320,title:'名著阅读',diff:2,q:'《鲁滨逊漂流记》作者是谁？',a:'笛福',e:'英国作家'},
    {id:321,title:'综合实践',diff:2,q:'开展\"读书分享会\"，需要准备什么？',a:'好书推荐、分享稿',e:'活动准备'}
];'''

# 找到合并母题的位置并添加五年级、六年级
old_all_topics = '''// 合并所有母题
const allTopics = {
    7: { math: topicsMath7, english: topicsEnglish7, chinese: topicsChinese7 },
    8: { math: topicsMath8, english: topicsEnglish8, chinese: topicsChinese8, physics: topicsPhysics8 },
    9: { math: topicsMath9, english: topicsEnglish9, chemistry: topicsChemistry9 }
};'''

new_all_topics = '''// 合并所有母题
const allTopics = {
    5: { math: topicsMath5, english: topicsEnglish5, chinese: topicsChinese5 },
    6: { math: topicsMath6, english: topicsEnglish6, chinese: topicsChinese6 },
    7: { math: topicsMath7, english: topicsEnglish7, chinese: topicsChinese7 },
    8: { math: topicsMath8, english: topicsEnglish8, chinese: topicsChinese8, physics: topicsPhysics8 },
    9: { math: topicsMath9, english: topicsEnglish9, chemistry: topicsChemistry9 }
};'''

content = content.replace(old_all_topics, new_all_topics)

# 在初三化学之前添加五年级和六年级数据
# 找到topicsChemistry9的位置，在其前面插入新数据

insert_position = content.find('// 初二物理21道')
if insert_position != -1:
    content = content[:insert_position] + grade5_math + grade6_math + '\n' + content[insert_position:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("母题数据修复完成!")
