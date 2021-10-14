// read_sonde.c
//
// read in sounding data and output height, temperature, and wind
// for plotting by gnuplot
//
// compile: gcc -o run_sonde read_sonde.c -lm
//
// input: radiosonde data (file must be specified below)
//
// output: height (m)  and temperature (C) data (temperature.txt)
//         height (m) and wind (u and v components) (m/s) data (winds.txt)
//
// functions:  convert_temp: takes in the temperature value from the file and 
//                  divides by ten, the outputs.
//             convert_winds: takes in the wind value from file (which is in 
//                  decimeters per second), and outputs the value in meters per 
//                  second.
//             radian_convert: takes in the wind direction and converts to radians.
//             calc_wind: takes in wind direction and speed, and an array of length
//                  two, converts wind to u and v coordinates, and stores those values
//                  in the array. No return value.
//
// written: G Mullendore, Jan. 2008
// modifications:  Lance Wilson, Jan. 2016
//

// include statements
#include <stdio.h>
#include <math.h>

// declare functions
float convert_temp(float temp_tenth);
float radian_convert(float wind_dir);
float convert_wind(float wind_speed_tenth);
void calc_wind(float wind_speed, float wind_dir, float winds[]);

// main program
int main()
{
  // declare variables
  float skip;  // skip unused variables from sounding
  float height, temp_tenth, temp, wind_dir, wind_dir_rad, wind_speed_tenth, wind_speed;
  float winds[2];

  int i;  // counter for loop
  const int header_length = 4;  // header length is constant
  char buff[256]; // array of characters to hold line of input file
  
  FILE *input, *temp_out, *wind_out;

  // open files
  input = fopen("BIS2016011800.txt","r");
  temp_out = fopen("temperature.txt","w");
  wind_out = fopen("winds.txt","w");

  // skip file header
  for (i=0; i<header_length; i++)
    fgets(buff,256,input);

  while(fgets(buff,256,input)) // while not end of file
  {
    // read height (m) and temperature (C*10) from sounding
    sscanf(buff,"%f %f %f %f %f %f %f",&skip,&skip,&height,&temp_tenth,&skip,&wind_dir,&wind_speed_tenth);

    // remove missing values
    if (temp_tenth != 99999)
    {
      // convert temperature
      temp = convert_temp(temp_tenth);

      // write variables to output file
      fprintf(temp_out,"%8.2f %8.2f\n",height,temp);     
    }

    // New if loop that does the same as the temp if loop, but with wind values.
    if (wind_dir != 99999 && wind_speed_tenth != 99999)
    {
      // Convert to radians.
      wind_dir_rad = radian_convert(wind_dir);
      // convert wind speed (still need to write function)
      wind_speed = convert_wind(wind_speed_tenth);

      // Convert to u and v coordinates.
      calc_wind(wind_dir_rad, wind_speed, winds);

      // Write height, u, and v variables to output file.
      fprintf(wind_out,"%8.2f %8.2f %8.2f\n",height,winds[0],winds[1]);     
    }

  }
}

// Converts temps from tenth of a degree to degree.
float convert_temp(float temp_tenth) 
{
  // declare local variables
  float temp;

  // convert from tenths of a degree to full degrees.
  temp = temp_tenth/10.0;

  return(temp);
}

// Converts the wind speed to radians.
float radian_convert(float wind_dir)
{
  float wind_rad;
  const double pi = 3.14159265358979;
  wind_rad = (270 - wind_dir) * pi/180;
  return wind_rad;
}

// Converts wind speed from tenths of a m/s to m/s.
float convert_wind(float wind_speed_tenth)
{
  float wind_speed;
  wind_speed = wind_speed_tenth/10.0;
  return wind_speed;
}

// Calculate u and v coordinates of the wind.
void calc_wind(float wind_dir, float wind_speed, float winds[])
{
  float u, v;
  u = -1 * wind_speed * sin(wind_dir);
  v = -1 * wind_speed * cos(wind_dir);
  winds[0] = u;
  winds[1] = v;
  return;
}

