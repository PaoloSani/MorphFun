import oscP5.*;
import netP5.*;
int PORT = 5005;
OscP5 oscP5;
NetAddress ip_port;

PImage img;
boolean rec;

void setup(){
  oscP5 = new OscP5(this,50050);
  ip_port = new NetAddress("127.0.0.1",PORT);
  
  size(1280, 720);
  background(0);
  
  img = loadImage("interfaccia2.png");

}


void sendClass(int instrument){
    OscMessage instrumentMessage = 
            new OscMessage("/selected_instrument"); 
    
    instrumentMessage.add("Instrument Chosen:");          
    instrumentMessage.add(instrument);  
    oscP5.send(instrumentMessage, ip_port);
    }
    
    
void sendRec(boolean recToggle){
    OscMessage recMessage = 
            new OscMessage("/rec_toggle"); 
    
    recMessage.add("Recording State:");                 
    recMessage.add(recToggle);  
    oscP5.send(recMessage, ip_port);
    }
    
  

  
void mousePressed(){              //user interaction
  int instrument = 0;
  String message = "no instrument selected";
   
  if(mouseX>3*width/7-30 & mouseX<4*width/7+30 & mouseY>3*height/4){   //rec  
      message = "Recording trigger";
      rec = !rec;
      sendRec(rec);  
  }
  if(rec==false){
    if(mouseX<width/2 & mouseY<height/2 & mouseY>height/6){
      instrument = 2;   //violin
      message = "Selected instrument: violin";
      sendClass(instrument);
    }
    if(mouseX>width/2 & mouseY<height/2 & mouseY>height/6){
      instrument = 1;    //flute
      message = "Selected instrument: flute";
      sendClass(instrument);
    }
    if(mouseX<width/2 & mouseY>height/2 & mouseY< 3*height/4){
      instrument = 3;     //trumpet
      message = "Selected instrument: trumpet";
      sendClass(instrument);
    }
    if(mouseX>width/2 & mouseY>height/2 & mouseY< 3*height/4){
      instrument = 4;     //sax
      message = "Selected instrument: sax";
      sendClass(instrument);
    }
  }
  //println(message);
  
  
}

void draw(){
  background(0);
  rectMode(CENTER);
  
  fill(190,100,70);        //flute
  rect(width/4,height/4+70,width/2, height/4);
  
  fill(50,100,120);      //sax
  rect(3*width/4,height/2+70,width/2, height/4);
  
  fill(180,190,40);        //violin
  rect(3*width/4,height/4+70,width/2, height/4);
  
  fill(130,50,130);        //trumpet
  rect(width/4,height/2+70,width/2, height/4);
  
  //fill(10,50,130);        //MORPHUN
  //rect(width/2,0.3*height/2-20,width/4+70, height/4-60);
  
  fill(180,50,50);        //REC
  ellipse(width/2, 1.7*height/2+12, width/4-40, height/4-30);
  
  fill(200,190,190);
  noStroke();
  rect(width/2,1.5*height/2-10,width, 5); 
  rect(width/2,height/6+30, width, 5);
  
  image(img,0,0);
  
  fill(255);
  ellipse(mouseX, mouseY, 10, 10);              //mouse
    
  
}
