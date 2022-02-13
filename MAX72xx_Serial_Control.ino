
#include <MD_MAX72xx.h>
#include <SPI.h>

#define HARDWARE_TYPE MD_MAX72XX::ICSTATION_HW
#define MAX_DEVICES 4
#define CLK_PIN   13
#define DATA_PIN  11
#define CS_PIN    10

// SPI hardware interface
MD_MAX72XX M = MD_MAX72XX(HARDWARE_TYPE, CS_PIN, MAX_DEVICES);

#define  DELAYTIME  500  // in milliseconds

int list[] = {(uint8_t)1,
                (uint8_t)2,
                (uint8_t)3,
                (uint8_t)4,
                (uint8_t)5,
                (uint8_t)6,
                (uint8_t)7,
                (uint8_t)8,
                (uint8_t)9,
                (uint8_t)25,
                (uint8_t)11,
                (uint8_t)12,
                (uint8_t)10,
                (uint8_t)10,
                (uint8_t)10,
                (uint8_t)35,
                (uint8_t)10,
                (uint8_t)10,
                (uint8_t)10,
                (uint8_t)10,
                (uint8_t)10,
                (uint8_t)10,
                (uint8_t)10,
                (uint8_t)35,
                (uint8_t)10,
                (uint8_t)10,
                (uint8_t)10,
                (uint8_t)10,
                (uint8_t)10,
                (uint8_t)10,
                (uint8_t)10,
                (uint8_t)35};
                
void setup()
{
  Serial.begin(500000);
  Serial.setTimeout(5);
  M.begin();
  M.control(MD_MAX72XX::UPDATE, MD_MAX72XX::OFF);
  for (int i = 0; i <= 32; i++) {
    M.setColumn(i, list[i]);
  }
  M.control(MD_MAX72XX::UPDATE, MD_MAX72XX::ON);
  delay(DELAYTIME);
}


String serialResponse = "";
char sz[132];

int nb = 0;
int s[32];

//Example of a message that has to be sent on Serial :
//001;002;003;004;005;006;007;008;009;010;011;012;013;014;015;016;017;018;019;020;021;022;023;024;025;026;027;028;029;030;031;032>

void loop() {
  if(Serial.available()){
    serialResponse = Serial.readStringUntil(">");
    char buf[sizeof(sz)];
    serialResponse.toCharArray(buf,sizeof(buf));
    char *p = buf;
    char *str;
    nb = 0;
    str = strtok_r(p,";",&p);
    while(str != NULL){
      s[nb] = atoi(str);
      nb += 1;
      str = strtok_r(p,";",&p);
    }
    if(nb == 32){
      M.control(MD_MAX72XX::UPDATE, MD_MAX72XX::OFF);
      for (int i = 0; i <= 32; i++) {
        M.setColumn(i, (uint8_t)s[i]);
      }
      M.control(MD_MAX72XX::UPDATE, MD_MAX72XX::ON);
    }
  }
}
