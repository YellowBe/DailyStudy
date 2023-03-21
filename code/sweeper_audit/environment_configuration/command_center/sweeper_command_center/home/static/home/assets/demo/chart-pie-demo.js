
    Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
    Chart.defaults.global.defaultFontColor = '#292b2c';
    var ctx = document.getElementById("myPieChart");
    var myPieChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: ['Sweeper1', 'Sweeper2', 'Sweeper3'],
        datasets: [{
        data: [2, 3, 1],
        backgroundColor: ['#007bff', '#dc3545', '#ffc107', '#28a745', '#123213'],
        }],
    },
    });
    