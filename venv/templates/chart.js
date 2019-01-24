function initHTML() {
    var input = document.getElementById("myText");
    input.addEventListener("keyup", function(event) {
        event.preventDefault();
        if (event.keyCode === 13) {
        document.getElementById("startButton").click();
        }
    });
}

function appendClassHeader(classIndex, text) {
    document.getElementsByClassName("tabcontent")[classIndex]
        .getElementsByTagName('h1')[0].innerHTML = text;
}

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

function createButtons(myColor) {
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
    buttonColor.setAttribute("onClick", "openParameter('Color', this, '" + myColor + "'); $('html, body').animate({scrollTop: 0}, 'medium')");
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
}

function removeElements() {
    $(".tablink").remove();
    $(".tabcontent").innerHTML = "";
    $(".svg-container").remove();
    d3.select("svg").remove();
}

function myFunction() {
    var x = document.getElementById("myText").value;
    var url = 'http://217.182.72.46:5000/?key=' + document.getElementById("myText").value;
    var xmlhttp = new XMLHttpRequest();
    var LabY;
    var LabX;
    var myColor;

    var inputText =  document.getElementById("myText");
    inputText.value = "";
    inputText.placeholder = "Provide spool ID";
    if(inputText.classList.contains('input-placeholder-red')) {
        inputText.classList.replace('input-placeholder-red', 'input-placeholder');
    }
    else {
        inputText.classList.add('input-placeholder');
    }

    xmlhttp.onreadystatechange = function() {
        try {
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

                if (my_data.color.includes("BLUE")) {
                    if(my_data.color.includes("NAVY")) {
                        myColor = "rgb(0, 0, 128)";
                    }
                    else
                    {
                        myColor = "blue";
                    }
                }

                else if (my_data.color.includes("RED")) {
                    myColor = "red";
                }

                areaMin = my_data.diameter - 0.02;
                areaMax = my_data.diameter + 0.02;

                var xm = (LabX.length / 10) + (LabX.length / 1000);
            }

            removeElements();
            createButtons(myColor);

            appendClassHeader(0, my_data.diameter + " mm");
            appendClassHeader(1, my_data.material);
            appendClassHeader(2, my_data.color + " | " + my_data.ral);
            appendClassHeader(3, my_data.mean.toFixed(3) + " mm");
            appendClassHeader(4, (my_data.ovality * 100).toFixed(1) + "%");
            appendClassHeader(5, (my_data.deviation * 1000).toFixed(1) + " μm");
            appendClassHeader(6, my_data.dateprod.substring(0, my_data.dateprod.length-9));

            document.getElementById("Color").style.backgroundColor = myColor;

            var classDiameter = document.getElementById("Diameter");
            var diameterParagraph = document.createElement("div");
            var descriptionDiameter = document.createElement("div");
            diameterParagraph.innerHTML = "Diameter";
            diameterParagraph.className = "parag";
            descriptionDiameter.innerHTML = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do <br>" +
                                            "eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut <br>" +
                                            "enim ad minim veniam, quis nostrud exercitation ullamco laboris <br>" +
                                            "nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in <br>" +
                                            "reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla <br>" +
                                            "pariatur. Excepteur sint occaecat cupidatat non proident, sunt in <br>" +
                                            "culpa qui officia deserunt mollit anim id est laborum.";
            descriptionDiameter.className = "descr";
            classDiameter.appendChild(diameterParagraph);
            classDiameter.appendChild(descriptionDiameter);

            var classMaterial = document.getElementById("Material");
            var materialParagraph = document.createElement("div");
            var descriptionMaterial = document.createElement("div");
            materialParagraph.innerHTML = "Material";
            materialParagraph.className = "parag";
            descriptionMaterial.innerHTML = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do <br>" +
                                            "eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut <br>" +
                                            "enim ad minim veniam, quis nostrud exercitation ullamco laboris <br>" +
                                            "nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in <br>" +
                                            "reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla <br>" +
                                            "pariatur. Excepteur sint occaecat cupidatat non proident, sunt in <br>" +
                                            "culpa qui officia deserunt mollit anim id est laborum.";
            descriptionMaterial.className = "descr";
            classMaterial.appendChild(materialParagraph);
            classMaterial.appendChild(descriptionMaterial);

            var classColor = document.getElementById("Color");
            var colorParagraph = document.createElement("div");
            var descriptionColor = document.createElement("div");
            colorParagraph.innerHTML = "Color | ColorRAL";
            colorParagraph.className = "parag";
            descriptionColor.innerHTML = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do <br>" +
                                        "eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut <br>" +
                                        "enim ad minim veniam, quis nostrud exercitation ullamco laboris <br>" +
                                        "nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in <br>" +
                                        "reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla <br>" +
                                        "pariatur. Excepteur sint occaecat cupidatat non proident, sunt in <br>" +
                                        "culpa qui officia deserunt mollit anim id est laborum.";
            descriptionColor.className = "descr";
            classColor.appendChild(colorParagraph);
            classColor.appendChild(descriptionColor);

            var classMean = document.getElementById("Mean");
            var meanParagraph = document.createElement("div");
            var descriptionMean = document.createElement("div");
            meanParagraph.innerHTML = "Mean diameter";
            meanParagraph.className = "parag";
            descriptionMean.innerHTML = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do <br>" +
                                        "eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut <br>" +
                                        "enim ad minim veniam, quis nostrud exercitation ullamco laboris <br>" +
                                        "nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in <br>" +
                                        "reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla <br>" +
                                        "pariatur. Excepteur sint occaecat cupidatat non proident, sunt in <br>" +
                                        "culpa qui officia deserunt mollit anim id est laborum.";
            descriptionMean.className = "descr";
            classMean.appendChild(meanParagraph);
            classMean.appendChild(descriptionMean);

            var classOvality = document.getElementById("Ovality");
            var ovalityParagraph = document.createElement("div");
            var descriptionOvality = document.createElement("div");
            ovalityParagraph.innerHTML = "Ovality";
            ovalityParagraph.className = "parag";
            descriptionOvality.innerHTML = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do <br>" +
                                           "eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut <br>" +
                                           "enim ad minim veniam, quis nostrud exercitation ullamco laboris <br>" +
                                           "nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in <br>" +
                                           "reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla <br>" +
                                           "pariatur. Excepteur sint occaecat cupidatat non proident, sunt in <br>" +
                                           "culpa qui officia deserunt mollit anim id est laborum.";
            descriptionOvality.className = "descr";
            classOvality.appendChild(ovalityParagraph);
            classOvality.appendChild(descriptionOvality);

            var classDeviation = document.getElementById("Deviation");
            var deviationParagraph = document.createElement("div");
            var descriptionDeviation = document.createElement("div");
            deviationParagraph.innerHTML = "Standard deviation";
            deviationParagraph.className = "parag";
            descriptionDeviation.innerHTML = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do <br>" +
                                             "eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut <br>" +
                                             "enim ad minim veniam, quis nostrud exercitation ullamco laboris <br>" +
                                             "nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in <br>" +
                                             "reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla <br>" +
                                             "pariatur. Excepteur sint occaecat cupidatat non proident, sunt in <br>" +
                                             "culpa qui officia deserunt mollit anim id est laborum.";
            descriptionDeviation.className = "descr";
            classDeviation.appendChild(deviationParagraph);
            classDeviation.appendChild(descriptionDeviation);

            var classDate = document.getElementById("Date");
            var dateParagraph = document.createElement("div");
            var descriptionDate = document.createElement("div");
            dateParagraph.innerHTML = "Date of production";
            dateParagraph.className = "parag";
            descriptionDate.innerHTML = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do <br>" +
                                        "eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut <br>" +
                                        "enim ad minim veniam, quis nostrud exercitation ullamco laboris <br>" +
                                        "nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in <br>" +
                                        "reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla <br>" +
                                        "pariatur. Excepteur sint occaecat cupidatat non proident, sunt in <br>" +
                                        "culpa qui officia deserunt mollit anim id est laborum.";
            descriptionDate.className = "descr";
            classDate.appendChild(dateParagraph);
            classDate.appendChild(descriptionDate);

            document.getElementById("defaultOpen").click();

            var margin = {top: 30, right: 150, bottom: 30, left: 35},
            width = 1500 - margin.left - margin.right,
            height = 250 - margin.top - margin.bottom;
            rawData = LabX.map(function(d, i){
              return { 'x': d, 'y' : LabY[i] };
            }),
            tempData = [
                    { x: 0.3, y0: areaMax, y1: areaMin, },
                    { x: xm, y0: areaMax, y1: areaMin, },
            ];

            data = [];
            var tempForTicksY = [];
            var tempForTicksX = [];

            var i;
            for (i = 0; i < LabX.length / 10; i++) {
                if (i % 50 == 0) {
                    tempForTicksX.push(i);
                }
            }

            var svg = d3.select("body")
                    .append("div")
                    .classed("svg-container", true)
                    .append("svg")
                    .attr("preserveAspectRatio", "xMinYMin meet")
                    .attr("viewBox", "0 0 " + width + " " + (height + margin.top + margin.bottom))
                    .classed("svg-content-responsive", true)
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
                tempForTicksY = [1.7, 1.73, 1.75, 1.77, 1.8];
            }
            else if (my_data.diameter == 2.85) {
                var scaleY = d3.scale.linear()
                            .domain([2.95, 2.75])
                            .range([0, height]);
                tempForTicksY = [2.75, 2.8, 2.83, 2.85, 2.87, 2.9, 2.95];
            }

            for(i = 0; i < rawData.length; i++)
                data.push({x: scaleX(rawData[i].x), y: scaleY(rawData[i].y)});
                         
            var xAxis = d3.svg.axis()
                         .scale(scaleX)
                         .orient("bottom").ticks(10)
                         .innerTickSize(-height)
                         .outerTickSize(0)
                         .tickValues(tempForTicksX)
                .tickFormat(function(d, i){
                    return d + 'm'
                })
                         .tickPadding(10);

            var yAxis = d3.svg.axis()
                         .scale(scaleY)
                         .orient("left")
                         .tickValues(tempForTicksY)
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

            var bisectDate = d3.bisector(function(d) { return d.x; }).left,
                formatValue = d3.format(",.3f"),
                formatDiameterValue = function(d) { return formatValue(d) + " mm"; },
                formatMetersValue = function(d) { return d + " m"};

            var focus = svg.append("g")
                .attr("class", "focus")
                .style("display", "none");

            focus.append("circle")
                .attr("r", 4.5);

            focus.append("text")
                .attr("x", -27)
                .attr("y", -15)
                .attr("dy", ".35em");

            svg.append("rect")
                .attr("class", "overlay")
                .attr("width", width)
                .attr("height", height)
                .on("mouseover", function() { focus.style("display", null); })
                .on("mouseout", function() { focus.style("display", "none"); })
                .on("mousemove", mousemove);

            function mousemove() {
                var x0 = scaleX.invert(d3.mouse(this)[0]),
                    i = bisectDate(rawData, x0, 1),
                    d0 = rawData[i - 1],
                    d1 = rawData[i],
                    d = x0 - d0.x > d1.x - x0 ? d1 : d0;
                focus.attr("transform", "translate(" + scaleX(d.x) + "," + scaleY(d.y) + ")");
                focus.select("text").text(formatDiameterValue(d.y));
            }

        } catch(err) {
            if (err.name == "SyntaxError") {
                inputText.placeholder = "Please, provide valid spool ID";
                if (inputText.classList.contains('input-placeholder')) {
                    inputText.classList.replace('input-placeholder', 'input-placeholder-red');
                }
                else {
                    inputText.classList.add('input-placeholder-red');
                }
            }
            else {
                console.log(err);
            }
        }
    };

    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}

function clickEvent() {
    myFunction();
}