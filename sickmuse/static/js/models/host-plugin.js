define(['underscore', 'backbone'], function (_, Backbone) {
    var HostPluginModel = Backbone.Model.extend({
        urlRoot : function () {
            return this.get('url');
        },
        parse: function(response) {
            var metrics = response.instances;
            var interval = null;
            var series = null;
            _.each(metrics, function (metric, key) {
                interval = (metric.end - metric.start) / metric.timeline.length;
                series = _.map(metric.timeline, function (value, index) {
                    var x = (metric.start + index * interval) * 1000,
                        y = value;
                    return [x, y];
                });
                metric.series = series;
                metric.active = true;
            });
            return {'metrics': metrics, 'units': response.units || null};
        },
        activeMetrics: function () {
            var metrics = {};
            _.each(this.get('metrics'), function (data, name) {
                if (data.active) {
                    metrics[name] = data;
                }
            });
            return metrics;
        },
        toggleSeries: function (label) {
            var metrics = this.get('metrics');
            metrics[label].active = !metrics[label].active;
        }
    });
    return HostPluginModel;
});
