define(['underscore', 'backbone'], function (_, Backbone) {
    var HostPluginModel = Backbone.Model.extend({
        urlRoot : function () {
            return this.get('url');
        },
        parse: function(response) {
            var metrics = response;
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
            });
            return {'metrics': metrics};
        }
    });
    return HostPluginModel;
});
