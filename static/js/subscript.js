/* The slide images are contained in the slides array. */
var slides2 = new Array('img/none.jpg');
//
$(document).ready(function(){
	/* This code is executed after the DOM has been completely loaded */

	$('.jiantou.zuo').click(function(){
		prev2();
		
		/* Clearing the autoadvance if we click one of the arrows */
		clearInterval(auto);

	});
	
	$('.jiantou.you').click(function(){
		next2();
		clearInterval(auto);
	});

	/* Preloading all the slide images: */

	for(var i=0;i<slides2.length;i++)
	{
		(new Image()).src=slides2[i];
	}
	
	/* Shoing the first one on page load: */
	transition2(1);
	
	
	/* Setting auto-advance every 10 seconds */
	
	var auto;
	
	auto=setInterval(function(){
		next2();
	},10*1000);
});

var current2 = {};
function transition2(id)
{
	/* This function shows the individual slide. */
	
	if(!slides2[id-1]) return false;
	
	if(current2.id)
	{
		/* If the slide we want to show is currently shown: */
		if(current2.id == id) return false;
		
		/* Moving the current slide layer to the top: */
		current2.layer.css('z-index',10);
		
		/* Removing all other slide layers that are positioned below */
		$('.mosaic-huadong').not(current2.layer).remove();
	}
	
	/* Creating a new slide and filling it with generateGrid: */
	var newLayer = $('<div class="mosaic-huadong">').html(generateGrid2({rows:7,cols:8,image:slides2[id-1]}));

	/* Moving it behind the current slide: */
	newLayer.css('z-index',1);

	$('#mosaic-huadongshow').append(newLayer);
	
	if(current2.layer)
	{
		/* Hiding each tile of the current slide, exposing the new slide: */
		$('.tile2',current2.layer).each(function(i){
			var tile2 = $(this);
			setTimeout(function(){
				tile2.css('visibility','hidden');
			},i*10);
		})
	}
	
	/* Adding the current id and newLayer element to the current object: */
	current2.id = id;
	current2.layer = newLayer;
}

function next2()
{
	if(current2.id)
	{
		transition2(current2.id%slides2.length+1);
	}
}

function prev2()
{
	if(current2.id)
	{
		transition2((current2.id+(slides2.length-2))%slides2.length+1);
	}
	
}

/* Width and height of the tiles in pixels: */
var tabwidth=60, tabheight=60;

function generateGrid2(param)
{
	/* This function generates the tile grid, with each tile containing a part of the slide image */
	
	/* Creating an empty jQuery object: */
	var elem = $([]),tmp;
	
	for(var i=0;i<param.rows;i++)
	{
		for(var j=0;j<param.cols;j++)
		{
			tmp = $('<div>', {
					"class":"tile2",
					"css":{
						"background":'#555 url('+param.image+') no-repeat '+(-j*tabwidth)+'px '+(-i*tabheight)+'px'
					}
			});
			
			/* Adding the tile to the jQuery object: */
			elem = elem.add(tmp);
		}
		
		/* Adding a clearing element at the end of each line. This will clearly divide the divs into rows: */
		elem = elem.add('<div class="clear2"></div>');
	}
	
	return elem;
}