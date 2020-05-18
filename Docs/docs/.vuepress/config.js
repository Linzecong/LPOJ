module.exports = {
    title: 'LPOJ 文档',
    description: 'LPOJ 的开发与使用文档',
    head: [
        ['link', { rel: 'icon', href: '/img/favicon.ico' }],
    ],
    base: '/',
    markdown: {
        lineNumbers: true // 代码块显示行号
    },
    themeConfig: {
        sidebarDepth: 5,
        nav: [
            { text: 'Demo', link: 'https://www.lpoj.cn/' },
            { text: 'GitHub首页', link: 'https://github.com/Linzecong/LPOJ/' },
            { text: '作者首页', link: 'https://github.com/Linzecong/' },
        ],

        sidebar: [
            {
                title: '开始上手',
                collapsable: true,
                children: [
                    '/faq/',
                    '/faq/intro',
                    '/faq/whatisoj',
                    '/faq/systemstruct'
                ]
            },
            {
                title: '部署文档',
                collapsable: true,
                children: [
                    '/deploy/',
                    '/deploy/frontend',
                    '/deploy/backend',
                    '/deploy/judgeserver',
                    '/deploy/judger',
                    '/deploy/crawlingserver'
                ]
            },
            {
                title: '开发文档',
                collapsable: true,
                children: [
                    '/dev/',
                    '/dev/frontend',
                    '/dev/backend',
                    '/dev/judgerserver',
                    '/dev/judger',
                ]
            },
            {
                title: '使用文档',
                collapsable: true,
                children: [
                    '/doc/',
                    '/doc/oj',
                    '/doc/judger',
                    '/doc/utils',
                    '/doc/faq',
                ]
            },
        ]

        
    },
    

}