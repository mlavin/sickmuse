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
            labelTemplate = _.template(
                '<a data-label="<%= label %>">' +
                '<span class="box-wrapper">' +
                '<span class="color-box" style="border: 5px solid <%= color %>;"></span>' +
                '</span>' +
                '<%= label %>' +
                '</a>'
            );
            this.legend = $('#' + this.$el.attr('id') + '-legend');
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
                    labelFormatter: function(label, series) {
                        return labelTemplate({label: label, color: series.color});
                    }
                }
            };
            this.model = new HostPluginModel({url: this.$el.data('url')});
            this.listenTo(this.model, "change", this.render);
            this.model.fetch();
        },
        render: function () {
            var self = this;
            this.graph(true);
            // Remove current legend to create a better one
            var oldLegend = $('.legend', this.$el).detach();
            $('tr', oldLegend).each(function (index, row) {
                self.legend.append(
                    $('<li>').append($('.legendLabel', row).html())
                );
            });
            var previousPoint = null;
            var template = this.tooltipTemplate;
            this.$el.bind("plothover", function (event, pos, item) {
                if (item) {
                    if (previousPoint !== item.dataIndex) {
                        previousPoint = item.dataIndex;
                        $("#tooltip").remove();
                        var x = item.datapoint[0].toFixed(2),
                            y = item.datapoint[1].toFixed(2);
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
            this.legend.on('click', 'li > a', function(e) {
                e.preventDefault();
                $(this).parent('li').toggleClass('disabled');
                self.model.toggleSeries($(this).data('label'));
                self.graph(false);
            });
        },
        graph: function(legend) {
            var series = _.map(this.model.activeMetrics(), function (data, name) {
                return {label: name, data: data.series};
            });
            this.plotOptions.legend.show = legend;
            this.plot = $.plot(this.$el, series, this.plotOptions);
        }
    });
    return PluginGraphView;
});
