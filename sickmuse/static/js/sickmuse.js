(function ($){
    $('.plugin-graph').each(function (i, elem) {
        var url = $(elem).data('url');
        var series = [];
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
            
            $.plot($(elem), series, {
                series: {
                    stack: true,
                    lines: {show: true, fill: true, steps: false}
                },
                xaxis: {mode: "time", timezone: "browser"},
                yaxis: {tickDecimals: 4},
                grid: {hoverable: true, clickable: true},
                legend: {
                    container: $('#' + $(elem).attr('id') + '-legend'),
                    labelFormatter: function(label, series) {
                        // Underscore or Handlebars would help here
                        return '<a href="#' + label + '">' + label + '</a>';
                    }
                }
            });

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
    })
})(jQuery);
