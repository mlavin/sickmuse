define(['jquery', 'underscore', 'backbone', 'models/host-plugin', 'flot',
    'flotstack', 'flottime', 'flotresize', 'flotzoom', 'scrollspy', 'collapse'], 
    function ($, _, Backbone, HostPluginModel) {
        var PluginGraphView = Backbone.View.extend({
            initialize: function () {
                var self = this;
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
                this.controls = $('#' + this.$el.attr('id') + '-controls');
                this.units = {
                    'bytes': {
                        tickDecimals: 2, 
                        tickFormatter: function suffixFormatter(val, axis) {
                            var sizes = ['', 'KB', 'MB', 'GB', 'TB'];
                            var posttxt = 0;
                            if (val === 0) return '0';
                            while (val >= 1024) {
                                posttxt++;
                                val = val / 1024;
                            }
                            return val.toFixed(axis.tickDecimals) + " " + sizes[posttxt];
                        }
                    }
                };
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
                    yaxis: {},
                    grid: {hoverable: true, clickable: true},
                    legend: {
                        labelFormatter: function(label, series) {
                            self.model.get("metrics")[label].color = series.color;
                            return labelTemplate({label: label, color: series.color});
                        }
                    },
                    selection: {mode: "x"}
                };
                // Event bindings
                var previousPoint = null;
                var template = this.tooltipTemplate;
                this.$el.bind("plothover", function (event, pos, item) {
                    if (item) {
                        if (previousPoint !== item.dataIndex) {
                            previousPoint = item.dataIndex;
                            $("#tooltip").remove();
                            var x = item.datapoint[0], y = 0,
                                datapoint = item.datapoint,
                                series = item.series,
                                yaxis = item.series.yaxis;
                            if (series.stack) {
                                y = item.datapoint[1] - item.datapoint[2];
                            } else {
                                y = item.datapoint[1];
                            }
                            $('body').append(template({
                                top: item.pageY + 5,
                                left: item.pageX + 5,
                                content: item.series.label + " " + yaxis.tickFormatter(y, yaxis)
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
                this.controls.on('change', ':input.date-range', function(e) {
                    self.model.fetch({data: {range: $(this).val()}});
                });
                this.controls.on('click', '.reset-zoom', function(e) {
                    e.preventDefault();
                    self.graph(false);
                });
                this.$el.bind("plotselected", function (event, ranges) {
                    self.graph(false, ranges.xaxis.from, ranges.xaxis.to);
                });
                this.model = new HostPluginModel({url: this.$el.data('url')});
                this.listenTo(this.model, "change", this.render);
                this.model.fetch();
            },
            render: function () {
                var self = this;
                this.graph(true);
                // Remove current legend to create a better one
                self.legend.html('');
                var oldLegend = $('.legend', this.$el).detach();
                $('tr', oldLegend).each(function (index, row) {
                    self.legend.append(
                        $('<li>').append($('.legendLabel', row).html())
                    );
                });
            },
            graph: function(legend, from, to) {
                var series = _.map(this.model.activeMetrics(), function (data, name) {
                    return {label: name, data: data.series, color: data.color || null};
                });
                var options = $.extend(true, {}, this.plotOptions);
                options.legend.show = legend;
                if (to && from) {
                    options.xaxis = $.extend(options.xaxis, {min: from, max: to});
                }
                var unit = this.model.get('units');
                var format = this.units[unit];
                if (unit && format) {
                    options.yaxis = $.extend(options.yaxis, format);
                }
                this.plot = $.plot(this.$el, series, options);
                if (from && to ) {
                    $('.reset-zoom', this.controls).show();
                } else {
                    $('.reset-zoom', this.controls).hide();
                }
            }
        });
    return PluginGraphView;
});
