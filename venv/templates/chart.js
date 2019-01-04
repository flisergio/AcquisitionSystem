function mainHeader() {
    d3.select('h1').style('color', 'black')
    .attr('class', 'heading')
    .style('font-size', '50px')
    .style('font-family', 'Georgia')
    .style('text-align', 'center')
    .style('text-decoration', 'overline underline')
    .style('text-decoration-style', 'dashed');
}
/*
function appendBody(t) {
    d3.select('body').append('p').text(t)
    .style('color', d3.rgb(125, 3, 155));
}
*/
function openParameter(parameterName, element, color) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablink");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].style.backgroundColor = "";
  }
  document.getElementById(parameterName).style.display = "block";
  element.style.backgroundColor = color;

}

function createButtons() {
    var buttonDiameter = document.createElement("button");
    var buttonDiameterText = document.createTextNode("Diameter");
    buttonDiameter.id = "defaultOpen";
    buttonDiameter.className = "tablink";
    buttonDiameter.appendChild(buttonDiameterText);
    buttonDiameter.setAttribute("onClick", "openParameter('Diameter', this, 'red'); $('html, body').animate({scrollTop: 0}, 'medium')");
    document.body.appendChild(buttonDiameter);

    var buttonMaterial = document.createElement("button");
    var buttonMaterialText = document.createTextNode("Material");
    buttonMaterial.className = "tablink";
    buttonMaterial.appendChild(buttonMaterialText);
    buttonMaterial.setAttribute("onClick", "openParameter('Material', this, 'rgb(255,137,0)'); $('html, body').animate({scrollTop: 0}, 'medium')");
    document.body.appendChild(buttonMaterial);

    var buttonColor = document.createElement("button");
    var buttonColorText = document.createTextNode("Color");
    buttonColor.className = "tablink";
    buttonColor.appendChild(buttonColorText);
    buttonColor.setAttribute("onClick", "openParameter('Color', this, 'rgb(255,230,0)'); $('html, body').animate({scrollTop: 0}, 'medium')");
    document.body.appendChild(buttonColor);

    var buttonMean = document.createElement("button");
    var buttonMeanText = document.createTextNode("Mean");
    buttonMean.className = "tablink";
    buttonMean.appendChild(buttonMeanText);
    buttonMean.setAttribute("onClick", "openParameter('Mean', this, 'green'); $('html, body').animate({scrollTop: 0}, 'medium')");
    document.body.appendChild(buttonMean);

    var buttonOvality = document.createElement("button");
    var buttonOvalityText = document.createTextNode("Ovality");
    buttonOvality.className = "tablink";
    buttonOvality.appendChild(buttonOvalityText);
    buttonOvality.setAttribute("onClick", "openParameter('Ovality', this, 'rgb(0,222,255)'); $('html, body').animate({scrollTop: 0}, 'medium')");
    document.body.appendChild(buttonOvality);

    var buttonDeviation = document.createElement("button");
    var buttonDeviationText = document.createTextNode("Deviation");
    buttonDeviation.className = "tablink";
    buttonDeviation.appendChild(buttonDeviationText);
    buttonDeviation.setAttribute("onClick", "openParameter('Deviation', this, 'blue'); $('html, body').animate({scrollTop: 0}, 'medium')");
    document.body.appendChild(buttonDeviation);

    var buttonDate = document.createElement("button");
    var buttonDateText = document.createTextNode("Date");
    buttonDate.className = "tablink";
    buttonDate.appendChild(buttonDateText);
    buttonDate.setAttribute("onClick", "openParameter('Date', this, 'purple'); $('html, body').animate({scrollTop: 0}, 'medium')");
    document.body.appendChild(buttonDate);

    var buttonGraph = document.createElement("button");
    var buttonGraphText = document.createTextNode("Go to graph");
    buttonGraph.className = "tablink";
    buttonGraph.appendChild(buttonGraphText);
    buttonGraph.setAttribute("onClick", "$('html, body').animate({scrollTop:$(document).height()}, 'slow')");
    document.body.appendChild(buttonGraph);
}

function myFunction() {
    var x = document.getElementById("myText").value;
    var url = 'http://217.182.72.46:5000/?key=' + document.getElementById("myText").value;
    var xmlhttp = new XMLHttpRequest();
    var LabY;
    var LabX;

    createButtons();

    xmlhttp.onreadystatechange = function() {
    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
        var my_data = JSON.parse(xmlhttp.responseText);

        LabX = my_data.labelY;
        LabY = my_data.labelX;

        var i;
        var memY1, memY2, memA;
        var j;
        for (j = 0; j < 1000; j++) {
            for (i = 0; i < (LabY.length - 1); i++) {
                memY1 = LabY[i];
                memY2 = LabY[i+1];
                memA = (memY1 + memY2)/2.0;
                LabY[i] = memY1 - (memY1 - memA)/2.0;
                LabY[i+1] = memY2 - (memY2 - memA)/2.0;
            }
        }

        areaMin = my_data.diameter - 0.02;
        areaMax = my_data.diameter + 0.02;

        var xm = (LabX.length / 10) + (LabX.length / 1000);
    }
    /*
    textDiameter = 'Diameter: ' + my_data.diameter;
    textMaterial = 'Material: ' + my_data.material;
    textColor = 'Color: ' + my_data.color;
    textMean = 'Mean diameter: ' + my_data.mean;
    textOvality = 'Ovality: ' + my_data.ovality;
    textDeviation = 'Standard deviation: ' + my_data.deviation;
    textDate = 'Date of production: ' + my_data.dateprod;

    appendBody(textDiameter);
    appendBody(textMaterial);
    appendBody(textColor);
    appendBody(textMean);
    appendBody(textOvality);
    appendBody(textDeviation);
    appendBody(textDate);
    */

    var classParagraph = document.createElement("p");

    var body = document.querySelector("body");

    var classDiameterParagraph = document.createTextNode(my_data.diameter + " milimeters");
    classParagraph.appendChild(classDiameterParagraph);
    var classDiameter = document.getElementById("Diameter");
    classDiameter.appendChild(classDiameterParagraph);

    var classMaterialParagraph = document.createTextNode(my_data.material);
    classParagraph.appendChild(classMaterialParagraph);
    var classMaterial = document.getElementById("Material");
    classMaterial.appendChild(classMaterialParagraph);

    var classColorParagraph = document.createTextNode(my_data.color);
    classParagraph.appendChild(classColorParagraph);
    var classColor = document.getElementById("Color");
    classColor.appendChild(classColorParagraph);

    var classMeanParagraph = document.createTextNode(my_data.mean + " milimeters");
    classParagraph.appendChild(classMeanParagraph);
    var classMean = document.getElementById("Mean");
    classMean.appendChild(classMeanParagraph);

    var classOvalityParagraph = document.createTextNode(my_data.ovality);
    classParagraph.appendChild(classOvalityParagraph);
    var classOvality = document.getElementById("Ovality");
    classOvality.appendChild(classOvalityParagraph);

    var classDeviationParagraph = document.createTextNode(my_data.deviation);
    classParagraph.appendChild(classDeviationParagraph);
    var classDeviation = document.getElementById("Deviation");
    classDeviation.appendChild(classDeviationParagraph);

    var classDateParagraph = document.createTextNode(my_data.dateprod);
    classParagraph.appendChild(classDateParagraph);
    var classDate = document.getElementById("Date");
    classDate.appendChild(classDateParagraph);

    document.getElementById("defaultOpen").click();

    var margin = {top: 20, right: 100, bottom: 30, left: 100},
    width = 1500 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;
    rawData = LabX.map(function(d, i){
      return { 'x': d, 'y' : LabY[i] };
    }),
    tempData = [
            { x: 0.3, y0: areaMax, y1: areaMin, },
            { x: xm, y0: areaMax, y1: areaMin, },
    ];
    data=[];

    var svg = d3.select("body").append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
            .style("stroke", "black")
            .style("stroke-width", 1)
            .style("fill", "none");    
              
    var scaleX = d3.scale.linear()
                .domain([0, xm])
                .range([0, width]);

    if (my_data.diameter == 1.75) {           
        var scaleY = d3.scale.linear()
                    .domain([1.8, 1.7])
                    .range([0, height]);
    }
    else if (my_data.diameter == 2.85) {
        var scaleY = d3.scale.linear()
                    .domain([2.95, 2.75])
                    .range([0, height]);
    }

    for(i = 0; i < rawData.length; i++)
        data.push({x: scaleX(rawData[i].x), y: scaleY(rawData[i].y)});
                 
    var xAxis = d3.svg.axis()
                 .scale(scaleX)
                 .orient("bottom").ticks(10)
                 .innerTickSize(-height)
                 .outerTickSize(0)
                 .tickPadding(10);

    var yAxis = d3.svg.axis()
                 .scale(scaleY)
                 .orient("left")
                 .innerTickSize(-width)
                 .outerTickSize(0)
                 .tickPadding(10);
               
    var area = d3.svg.area()
        .x(function(d) { return scaleX(d.x); })
        .y0(function(d) { return scaleY(d.y0); })
        .y1(function(d) { return scaleY(d.y1); });

    var line = d3.svg.line()
        .x(function(d){return d.x;})
        .y(function(d){return d.y;});

    svg.append("g")      
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis)
     
    svg.append("g") 
        .attr("class", "y axis")
        .call(yAxis);

    svg.append("path")
    .datum(tempData)
    .attr("class", "area")
    .attr("d", area);

    svg.append("path")
        .data([data])
        .attr("class", "line")
        .attr("d", line);
    };

    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}

function clickEvent() {
    myFunction();
}