define(['jquery', 'underscore', 'backbone', 'models/host-plugin', 'flot',
    'flotstack', 'flottime', 'flotresize', 'scrollspy'], function ($, _, Backbone, HostPluginModel) {
    var PluginGraphView = Backbone.View.extend({
        initialize: function () {
            this.plot = null;
            this.tooltipTemplate = _.template(
                '<div id="tooltip" class="tooltip tip fade in" ' +
                'style="display: block; top: <%= top %>px; left: <%= left %>px;">' +
                '<div class="tooltip-arrow"></div>' +
                '<div class="tooltip-inner"><%= content %></div>' +
                '</div>'
            );
            labelTemplate = _.template('<a class="badge"><%= label %></a>');
            this.plotOptions = {
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
                    container: $('#' + this.$el.attr('id') + '-legend'),
                    labelFormatter: function(label, series) {
                        return labelTemplate({label: label});
                    }
                }
            };
            this.model = new HostPluginModel({url: this.$el.data('url')});
            this.listenTo(this.model, "change", this.render);
            this.model.fetch();
        },
        render: function () {
            var series = _.map(this.model.get('metrics'), function (data, name) {
                return {label: name, data: data.series};
            });
            this.plot = $.plot(this.$el, series, this.plotOptions);
            var previousPoint = null;
            var template = this.tooltipTemplate;
            this.$el.bind("plothover", function (event, pos, item) {
                if (item) {
                    if (previousPoint !== item.dataIndex) {
                        previousPoint = item.dataIndex;
                        $("#tooltip").remove();
                        var x = item.datapoint[0].toFixed(2),
                            y = item.datapoint[1].toFixed(2);
                        var html = template({
                            top: item.pageY + 5,
                            left: item.pageX + 5,
                            content: item.series.label + " " + y
                        });
                        console.log(html);
                        $('body').append(template({
                            top: item.pageY + 5,
                            left: item.pageX + 5,
                            content: item.series.label + " " + y
                        }));
                    }
                }
                else {
                    $("#tooltip").remove();
                    previousPoint = null;            
                }
            });
        }
    });
    return PluginGraphView;
});
