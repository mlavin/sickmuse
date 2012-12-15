var jQueryPluginShim = {exports: 'jQuery', deps: ['jquery']};
var flotPluginShim = {exports: 'jQuery', deps: ['flot']};

require.config({
    paths: {
        jquery: '../libs/jquery/jquery',
        flot: '../libs/flot/jquery.flot',
        flotstack: '../libs/flot/jquery.flot.stack',
        flottime: '../libs/flot/jquery.flot.time',
        flotresize: '../libs/flot/jquery.flot.resize',
        scrollspy: '../libs/bootstrap/js/bootstrap-scrollspy'
    },
    shim: {
        flot: jQueryPluginShim,
        flotstack: flotPluginShim,
        flottime: flotPluginShim,
        flotresize: flotPluginShim,
        scrollspy: jQueryPluginShim
    }
});

require(['jquery', 'flot', 'flotstack', 'flottime', 'flotresize', 'scrollspy'], function ($) {
    (function ($){
        $('.plugin-graph').each(function (i, elem) {
            var url = $(elem).data('url');
            var series = [];
            var id = $(elem).attr('id');
            $.getJSON(url, function (data) {
                // Fetch data and build the graph
                series = [];
                // Underscore would help here
                $.each(data, function (key, metric) {
                    var interval = (metric.end - metric.start) / metric.timeline.length;
                    var timeline = metric.timeline.map(function (value, index) {
                        var x = (metric.start + index * interval) * 1000,
                            y = value;
                        return [x, y];
                    });
                    series.push({
                        label: key,
                        data: timeline
                    });
                });
                
                var plot = $.plot($(elem), series, {
                    colors: ["#DE5090", "#84C7E2", "#F7BECA", '#F2355B', '#FFDAC9', "#D4EDF4" ],
                    series: {
                        stack: true,
                        lines: {
                            show: true,
                            fill: true,
                            steps: false,
                            lineWidth: 1
                        },
                        shadowSize: 1
                    },
                    xaxis: {mode: "time", timezone: "browser"},
                    yaxis: {tickDecimals: 3},
                    grid: {hoverable: true, clickable: true},
                    legend: {
                        container: $('#' + id + '-legend'),
                        labelFormatter: function(label, series) {
                            // Underscore or Handlebars would help here
                            return '<a class="badge">' + label + '</a>';
                        }
                    }
                });
                // Store the plot and the original data set
                $(elem).data('series', series);            
                $(elem).data('plot', plot);

                var previousPoint = null;
                $(elem).bind("plothover", function (event, pos, item) {
                    if (item) {
                        if (previousPoint != item.dataIndex) {
                            previousPoint = item.dataIndex;
                            
                            $("#tooltip").remove();
                            var x = item.datapoint[0].toFixed(2),
                                y = item.datapoint[1].toFixed(2);

                            // Underscore or Handlebars would help here
                            $('<div>', {id: 'tooltip'})
                                .addClass("tooltip tip fade in")
                                .css({
                                    display: 'block',
                                    top: item.pageY + 5,
                                    left: item.pageX + 5,
                                }).append(
                                    $('<div>').addClass('tooltip-arrow')
                                ).append(
                                    $('<div>').addClass('tooltip-inner')
                                        .text(item.series.label + " " + y)
                                ).appendTo("body");
                        }
                    }
                    else {
                        $("#tooltip").remove();
                        previousPoint = null;            
                    }
                });
                
            });
        });
    })(jQuery);
});
