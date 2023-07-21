// folder to scan for SVG files
var inputFolder = Folder.selectDialog();
var files = inputFolder.getFiles("*.svg");

// create 'export' folder if it doesn't exist
var outputFolder = new Folder(inputFolder.fsName + '/export_512');
if (!outputFolder.exists) {
    outputFolder.create();
}

var count = 0;
var checkpoint = 0;
var logFile = new File(outputFolder.fsName + '/log.txt');
logFile.open('a'); // Open file for appending

// loop through all files
for (var i = 0; i < files.length; i++) {
    
    // Check if the file already exists, if so skip this iteration
    if(count >= checkpoint){    
        try {
            var fileName = files[i].name.substring(0, files[i].name.lastIndexOf('.'));
            var pngFileName = outputFolder.fsName + "/" + fileName + ".png";
            var pngFile = new File(pngFileName);
            var doc = app.open(files[i]); // open the document
            var scaleFactor = Math.min(512 / doc.width, 512 / doc.height);
            var width  = 512;
            var height = 512;
            var abBounds = doc.artboards[0].artboardRect; // left, top, right, bottom
            var ableft   = abBounds[0];
            var abtop    = abBounds[1];
            var abwidth  = abBounds[2] - ableft;
            var abheight = abtop - abBounds[3];
            var abctrx   = abwidth / 2 + ableft;
            var abctry   = abtop - abheight / 2;
            var ableft   = abctrx - width  / 2;
            var abtop    = abctry + height / 2;
            var abright  = abctrx + width  / 2;
            var abbottom = abctry - height / 2;
    
            doc.artboards[0].artboardRect = [ableft, abtop, abright, abbottom];
            

            // put all elements in a group then resize it
            // alert(app.activeDocument.activeLayer.pageItems.length)
            var group = doc.groupItems.add();
            
            while (app.activeDocument.activeLayer.pageItems.length > 1) {
                app.activeDocument.activeLayer.pageItems[1].move(group, ElementPlacement.INSIDE);
                
            }
            // group.resize(scaleFactor * 80, scaleFactor * 80, true, false, false, false, scaleFactor * 135); 
            group.resize(scaleFactor * 80, scaleFactor * 80, true, true, true, true, scaleFactor * 135, Transformation.CENTER); 


            // var group = doc.groupItems.add();
            // var itemSize = app.activeDocument.activeLayer.pageItems.length
            // // alert('itemSize = ' + itemSize)
            // for (var j = 1; j < itemSize+1; j++) {
            //     // alert('j = ' + j)
            //     doc.pageItems[j].move(group, ElementPlacement.INSIDE);
            // }
            // group.resize(scaleFactor * 80, scaleFactor * 80, true, false, false, false, scaleFactor * 135);    


            // save png
            var pngExportOptions = new ExportOptionsPNG24();
            pngExportOptions.transparency = false;
            pngExportOptions.artBoardClipping = true;
                    
        }
        catch(e) {
            logFile.writeln('Error with file: ' + files[i].name + ' at count: ' + i);
            logFile.writeln('Error message: ' + e.message);
            continue
        }
        doc.exportFile(pngFile, ExportType.PNG24, pngExportOptions);
        doc.close(SaveOptions.DONOTSAVECHANGES);
    }
    count +=1
    
}


