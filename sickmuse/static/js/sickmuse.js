require.config({
    paths: {
        jquery: '../libs/jquery/jquery',
        flot: '../libs/flot/jquery.flot',
        flotstack: '../libs/flot/jquery.flot.stack',
        flottime: '../libs/flot/jquery.flot.time',
        flotresize: '../libs/flot/jquery.flot.resize',
        flotzoom: '../libs/flot/jquery.flot.selection',
        scrollspy: '../libs/bootstrap/js/bootstrap-scrollspy',
        collapse: '../libs/bootstrap/js/bootstrap-collapse',
        backbone: '../libs/backbone/backbone',
        underscore: '../libs/underscore/underscore'
    },
    shim: {
        flot: {exports: 'jQuery', deps: ['jquery']},
        flotstack: {exports: 'jQuery', deps: ['flot']},
        flottime: {exports: 'jQuery', deps: ['flot']},
        flotresize: {exports: 'jQuery', deps: ['flot']},
        flotzoom: {exports: 'jQuery', deps: ['flot']},
        scrollspy: {exports: 'jQuery', deps: ['jquery']},
        collapse: {exports: 'jQuery', deps: ['jquery']},
        backbone: {
            deps: ['underscore', 'jquery'],
            exports: 'Backbone'
        },
        underscore: {
            exports: '_'
        }
    }
});

require(['jquery', 'views/plugin-graph'], function ($, PluginGraphView) {
    $('.plugin-graph').each(function (i, elem) {
        var view = new PluginGraphView({'el': $(elem)});
    });
});
