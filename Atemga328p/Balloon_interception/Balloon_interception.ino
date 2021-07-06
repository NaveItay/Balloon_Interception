#include <Servo.h>
char input = ' '; //serial input is stored in this variable

Servo horizontal_servo;
Servo vertical_servo;

#define horizontal 3
#define vertical 2
#define laser 8

int x = 360 / 2;
int y = 180 / 2;

int servoVal;
bool laser_flag = false; 

void setup() {
  Serial.begin(9600);
   
  horizontal_servo.attach(horizontal);
  vertical_servo.attach(vertical);

  horizontal_servo.write(x);
  vertical_servo.write(y);

  // Laser configuration   
  pinMode(laser, OUTPUT);
  laser_flag = false;

}
 
void loop() {

  // debug  
  Serial.print("x = ");
  Serial.println(x);
  
  Serial.print("y = ");
  Serial.println(y);
 
  if ( Serial.available() )
  {
    input = Serial.read();          // reads the data into a variable

    switch (input)
    {
      case 'U': // Motor Up  
      {       
        // Laser OFF      
        laser_flag = false; 
        
        if (y < 180){
         y += 1;                     // updates the value of the angle
         vertical_servo.write(y);    // adjusts the digital servo angle according to the input
        }
        break;
      }
      case 'D': // Motor Down  
      {  
        // Laser OFF      
        laser_flag = false;
        
        if (y > 0){
         y -= 1;
         vertical_servo.write(y);
        }
        break;
      }
      case 'L': // Motor Left
      { 
        // Laser OFF      
        laser_flag = false;
        
        if (x > 0){
          x -= 1;  
          horizontal_servo.write(x);
        }
        break;
      }
      case 'R': // Motor Right
      { 
        // Laser OFF      
        laser_flag = false;
        
        if (x < 360){
        x += 1;
        horizontal_servo.write(x);
        }
        break;
      }
      case 'S': // Laser ON
      { 
        laser_flag = true;
        break;
      }
      case 'O': // Laser OFF
      { 
        laser_flag = false;
        break;
      }
    }

  if (laser_flag == true)
  {
    digitalWrite(laser, LOW);
  }
  else digitalWrite(laser, HIGH);
  
  input = ' '; // Clear
    
  } // Close if Serial.available()  
} // Close loop
