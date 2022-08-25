function include(file) {
    const script = document.createElement('script');
    script.src = file;
    script.type = 'text/javascript';
    script.defer = true;

    document.getElementsByTagName('head').item(0).appendChild(script);
}

if (scenario === 'solar') {
    include('/../../static/geochart_markers.js');
} else {
    include('/../../static/geochart_countries.js');
}
