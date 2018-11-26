/*
 * hoe toets mens of die element warm word of nie? idee is gee max power vir 20 sekondes kyk of temp ten minste een graad opgaan?
 */


#include "math.h"
#include "stdio.h"
#include <DS3231.h>//for rtc
#include "string.h"
#include <LiquidCrystal.h>
// Init the DS3231 using the hardware interface
DS3231  rtc(SDA, SCL);
char buft[10];
char bufa[10];
//------------this section of variables is for the temperature sensor--------------//
  int temp=10;
  #define  InVol 5.02
  #define  Cal 273
  #define  A_1 0.003354016
  #define  B_1 0.0002569850
  #define  C_1 0.000002620131
  #define  D_1 0.00000006383091
  #define  R_1 1000
  #define  gain 2.5
  #define  R_2 1500
  #define  R_ref 10000
  #define  decimals 2
  #define  M 0.00488678556
  double E=0;
  double temperature=0;
  double v=0;
//----------------------------------------this section of variables is for the current sensor------------------------//
#define mvPerAmp 66
int rawRead=0;
int ACSoffset=2495;
double Voltage=0;
double Amps=0;
int maxvolt=0;
double factor=0;
//----------------------------------------this section of variables is for period counting--------------------//
volatile int count=0;
volatile int period=0;
volatile int power=0;
//-----------------------------------------this section is for instructions from the serial port--------//
int mode=3;
unsigned int setTemp=0;
int heat=1;
String inputString="";
String currentInstruction="mode:2temp:060";////////////////////////////////test mode
//String currentInstruction="mode:3temp:060";////////////////////////////////actual running mode comment test mode line above for final demonstration
bool stringComplete=false;
//----------------------------------------//
int death=0;//this is the variable that determines lockout mode where eternal intervention is required to reset(just switch off and on again)
//--------------------------------------//
int count1=0;
LiquidCrystal lcd(7,8,9,10,11,12);//setup pins for lcd

void setup()
{
  //set up lcd rows and columns
   lcd.begin(16, 2);
// start serial communication at this rate
  Serial.begin(115200);
  inputString.reserve(200);
  currentInstruction.reserve(200);
  //setpin A0 as an analog input for the temperature sensor reading
  pinMode(A0,INPUT);
  pinMode(A1,INPUT);
  pinMode(2,INPUT);///zerocross
  pinMode(22,OUTPUT);//opto
    pinMode(52, OUTPUT);//fan

  rtc.begin();
  // The following lines can be uncommented to set the date and time
 /* rtc.setDOW(WEDNESDAY);     // Set Day-of-Week to SUNDAY
  rtc.setTime(8, 59, 00);     // Set the time to 12:00:00 (24hr format)
  rtc.setDate(07, 11, 2018);   // Set the date to January 1st, 2014*/
  
attachInterrupt(digitalPinToInterrupt(2),counter,FALLING);
}
//*******************************************kyk na die logika van die stuk********************//
void counter()//ISR to count periods elapsed up to 10 and restart counting and creates digital output on opto pin to switch triac on and off.
{
    
 
        if(power==10)
        {
          digitalWrite(22,HIGH);//switch opto on
        }

        
      if(power==0)
      {
        digitalWrite(22,LOW);
      }

      
      if(power>0 && power<10)
      {
        count++;
             if(count==2)//a full period has passed
             {
                period++;
                  if(period<=power)
                  {
                    digitalWrite(22,HIGH);
                   // Serial.println("on");
                  }
                  if(period>power&&period!=10)
                  {
                    digitalWrite(22,LOW);//switch opto off
                    //Serial.println("off");
                  }
                    if(period==10)
                  {
                    period=0; 
                     digitalWrite(22,LOW);//switch opto off
                    // Serial.println("off");
                  }
              count=0;
          }

      }
       
}

void serialEvent()//recieve input string from serial communication
{
  while(Serial.available())
  {
    char inChar=(char)Serial.read();//gets the next byte
    inputString+=inChar;

    if(inChar==' ')//space character recieved means fully recieved
    {
      stringComplete=true;
    }

        //-----------determine what has been sent serially---------------------------------//
    if(stringComplete)
    {
      currentInstruction=inputString;
      if(currentInstruction[0]!='m'||currentInstruction[3]!='e'||currentInstruction[6]!='t'||currentInstruction[9]!='p')
      {
        currentInstruction="mode:3temp:001";
        Serial.println("x");
        Serial.println("x");
        Serial.println("x");
        Serial.println("x");
        Serial.println("x");
      }
      //Serial.println(currentInstruction); //tester line to see if currentinstruction holds the instruction serially recieved
      inputString="";
      stringComplete=false;
    }
  }

}

//function to concatenate two integers used to extract values from recieved instruction
unsigned int concatenate(unsigned int x, unsigned int y)
{
  unsigned int power=10;
  while(y>= power)
  {
    power *=10;
  }
  return x*power+y;
  
}

void loop() 
{   
          //---------Insert a section to concatenate the recieved instructions-----------------//
          
            mode=currentInstruction[5]-'0';//retrieves the current status of test as an integer
           //this section combines the three possible character locations for the set temperaure and then forms an integer from it by concatenating the three variables
            unsigned int t1=currentInstruction[11]-'0';
            unsigned int t2=currentInstruction[12]-'0';
            unsigned int t3=currentInstruction[13]-'0';
            int temporary=concatenate(t1,t2);
            setTemp=concatenate(temporary,t3);
           
          
          

          if(mode==1)//self test
          {
             digitalWrite(52,LOW);//fan off
            //print to lcd selft test mode
             power=0;
             lcd.setCursor(0, 0);
             lcd.print("Mode: Self-Test");
             v=analogRead(A0);
             rawRead=analogRead(A1);
            
             if(v==1023||v==0)
             {
              Serial.println("T:0H:1");
              Serial.println("Device will not run");
              lcd.setCursor(0, 0);
              lcd.print("MALFUNCTION    ");
              death=1;
              while(death==1)//this piece ensures you stay stuck until power has been removed and test runs again
              {
                lcd.setCursor(0, 1);
                lcd.print("Repair!!!");
                delay(500);
                power=0;
              }
             }
               //nuwe code
             power=10;
             digitalWrite(52,HIGH);
             for(int p=0;p<10;p++)
             {
              delay(2000);//heat the element for 20 seconds
             }
             int temp_v=analogRead(A0);
             if((v+3)>=temp_v)
             {
              Serial.println("T:1H:0");
                death=1;
              while(death==1)//this piece ensures you stay stuck until power has been removed and test runs again
              {
                lcd.setCursor(0, 1);
                lcd.print("Repair!!!");
                delay(500);
                power=0;
              }
             }
             //nuwe code end

             
             else{Serial.println("T:1H:1");}
             delay(3000);
          }

         if(mode==2)//active
         {
          //print to lcd active
             //fan on
            //delay(4);//every decisecond  at least
            //---------------tester lines---------------------------//
            //Serial.println(setTemp);//testing purposes
            //Serial.println(rtc.getDOWStr());
            //Serial.print(" ");
            //Serial.print(rtc.getDateStr());
            //Serial.print("-");
            //Serial.print(rtc.getTimeStr());           
            //----------------------------------------------------//
            String datum=rtc.getDateStr();
            String tyd=rtc.getTimeStr();
            String dash="-";
            String space=" ";
            //------------------temperature reading section-------//
            for(int i=0;i<=200;i++)
            {
              v+=analogRead(A0);
            }
              //v=analogRead(A0);
             v=v/200;
              v=v*M;
              E=(log((R_1*(InVol/v)*gain-R_1-R_2)/(R_ref)));
              temperature=1/((A_1+B_1*E+C_1*E*E+D_1*E*E*E))-Cal;
              v=0;
            //-------------------current reading section--------------//
               maxvolt=0;
                     for(int i=0;i<950;i++)//take 800 readings to get the max as that is max of your sine wave
                      {
                          rawRead=analogRead(A1);
                          if(rawRead>maxvolt)//actually max voltage
                          {
                            maxvolt=rawRead;
                          }
                      }
                    
               
              
                 Voltage=(maxvolt/1024.0)*5000;//gives mV
                  Amps=((Voltage-ACSoffset)/mvPerAmp);
                  Amps=Amps*0.707;//rms value
                  Amps=factor*Amps;
                  
           
              if(Amps<=0)
              {
                Amps=0;
              }
             /* Serial.print("Amps:");
              Serial.print(Amps,2);
              Serial.print("Temp:");
              Serial.print(temperature,2);*/
              String amps="A";
              //String ampread=Amps;
              String temp="T";
              String d="D";
              String serialout=d+datum+dash+tyd+dash+amps+Amps+temp+temperature+space;
              Serial.println(serialout);///////////////////////////////////////////////////////////////////////////////////////////////jyt hier gechange na ln
              if(count1==0||count1==10)//100 because 100*10milliseconds will thus update the lcd every second
            {
               lcd.setCursor(0, 0);
              lcd.print("Mode: Active   ");
              lcd.setCursor(0,1);   
              lcd.print("Water temp:");
              lcd.print(temperature,1);
            }
            count1++;
            if(count1>10)
            {
              count1=0;
            }
              
             //---------------------Determine power level--------------//
                if((setTemp-temperature)>6)
                    {
                      power=10;
                      digitalWrite(52,HIGH);
                    }
                     if((setTemp-temperature)<0.4)//set this to switch off heat sooner or later
                    {
                      power=0;
                      digitalWrite(52,LOW);
                       
                    }
                    if((setTemp-temperature)<=6 &&(setTemp-temperature)>=0.4)
                    {
                       power=3+round((setTemp-temperature));//returns a percentage of power this number represents the number of periods to be on 
                       digitalWrite(52,HIGH);
                    } 
                  factor=power*0.1;
             // Serial.print("power output: ");//code test lines remove when done
             // Serial.println(factor);
           
         }
     if(mode==3)//Inactive
     {
      power=0;
      digitalWrite(52,LOW);
        lcd.setCursor(0, 0);
        lcd.print("Mode: Inactive  ");
      }

      
          
}
   
