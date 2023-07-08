// folder to scan for SVG files
var inputFolder = Folder.selectDialog();
var files = inputFolder.getFiles("*.svg");

// create 'export' folder if it doesn't exist
var outputFolder = new Folder(inputFolder.fsName + '/export');
if (!outputFolder.exists) {
    outputFolder.create();
}

// loop through all files
for (var i = 0; i < files.length; i++) {

    var pngFileName = outputFolder.fsName + "/" + files[i].name.split(".")[0] + ".png";
    var pngFile = new File(pngFileName);
    
    // Check if the file already exists, if so skip this iteration
    if(!pngFile.exists){

        var doc = app.open(files[i]); // open the document
        var scaleFactor = Math.min(1024 / doc.width, 1024 / doc.height);
    
        // adjust the artboard size
        try {
            var width  = 1024;
            var height = 1024;
            var abBounds = doc.artboards[0].artboardRect; // left, top, right, bottom
    
            var ableft   = abBounds[0];
            var abtop    = abBounds[1];
            var abwidth  = abBounds[2] - ableft;
            var abheight = abtop- abBounds[3];
    
            var abctrx   = abwidth / 2 + ableft;
            var abctry   = abtop - abheight / 2;
    
            var ableft   = abctrx - width  / 2;
            var abtop    = abctry + height / 2;
            var abright  = abctrx + width  / 2;
            var abbottom = abctry - height / 2;
    
            doc.artboards[0].artboardRect = [ableft, abtop, abright, abbottom];
        
        }
        catch(e) {
            alert(e.message);
        }
    
        // group all items in the document
        // alert(doc.groupItems.length)
        if (doc.groupItems.length <= 1){       // if no group
            var group = doc.pageItems[0];   
        }else{
            var group = doc.groupItems[1];      // if there are groups
        }
    
        // resize the group
        group.resize(scaleFactor * 80, scaleFactor * 80, true, true, true, true, scaleFactor * 140);
        
        var pngExportOptions = new ExportOptionsPNG24();
        pngExportOptions.transparency = false;
        pngExportOptions.artBoardClipping = true;
    
        doc.exportFile(pngFile, ExportType.PNG24, pngExportOptions);
        doc.close(SaveOptions.DONOTSAVECHANGES);
    
    }
    
}
