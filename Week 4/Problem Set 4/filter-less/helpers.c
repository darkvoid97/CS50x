#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Take average of red, green, and blue
            int average = round(((float)image[i][j].rgbtRed + (float)image[i][j].rgbtGreen + (float)image[i][j].rgbtBlue)/3);
            // Update pixel values
            image[i][j].rgbtRed = image[i][j].rgbtBlue = image[i][j].rgbtGreen = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Compute sepia values
            int r = image[i][j].rgbtRed;
            int g = image[i][j].rgbtGreen;
            int b = image[i][j].rgbtBlue;
            int sepia_r = round(0.393 * r + 0.769 * g + 0.189 * b);
            int sepia_g = round(0.349 * r + 0.686 * g + 0.168 * b);
            int sepia_b = round(0.272 * r + 0.534 * g + 0.131 * b);
            // Update pixel with sepia values
            if (sepia_r > 255)
                image[i][j].rgbtRed = 255;
            else
                image[i][j].rgbtRed = sepia_r;
            if (sepia_g > 255)
                image[i][j].rgbtGreen = 255;
            else
                image[i][j].rgbtGreen = sepia_g;
            if (sepia_b > 255)
                image[i][j].rgbtBlue = 255;
            else
                image[i][j].rgbtBlue = sepia_b;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < (width/2); j++)
        {
            // Swap pixels
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - (j + 1)];
            image[i][width - (j + 1)] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create a copy of image
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sum_blue;
            int sum_green;
            int sum_red;
            float counter;
            sum_blue = sum_green = sum_red = counter = 0;

            if (i >= 0 && j >= 0)
            {
                sum_red += copy[i][j].rgbtRed;
                sum_green += copy[i][j].rgbtGreen;
                sum_blue += copy[i][j].rgbtBlue;
                counter++;
            }

            if (i >= 0 && j - 1 >= 0)
            {
                sum_red += copy[i][j-1].rgbtRed;
                sum_green += copy[i][j-1].rgbtGreen;
                sum_blue += copy[i][j-1].rgbtBlue;
                counter++;
            }

            if (i - 1 >= 0 && j >= 0)
            {
                sum_red += copy[i-1][j].rgbtRed;
                sum_green += copy[i-1][j].rgbtGreen;
                sum_blue += copy[i-1][j].rgbtBlue;
                counter++;
            }

            if (i - 1 >= 0 && j - 1 >= 0)
            {
                sum_red += copy[i-1][j-1].rgbtRed;
                sum_green += copy[i-1][j-1].rgbtGreen;
                sum_blue += copy[i-1][j-1].rgbtBlue;
                counter++;
            }

            if ((i >= 0 && j + 1 >= 0) && (i >= 0 && j + 1 < width))
            {
                sum_red += copy[i][j+1].rgbtRed;
                sum_green += copy[i][j+1].rgbtGreen;
                sum_blue += copy[i][j+1].rgbtBlue;
                counter++;
            }

            if ((i - 1 >= 0 && j + 1 >= 0) && (i - 1 >= 0 && j + 1 < width))
            {
                sum_red += copy[i-1][j+1].rgbtRed;
                sum_green += copy[i-1][j+1].rgbtGreen;
                sum_blue += copy[i-1][j+1].rgbtBlue;
                counter++;
            }

            if ((i + 1 >= 0 && j >= 0) && (i + 1 < height && j >= 0))
            {
                sum_red += copy[i+1][j].rgbtRed;
                sum_green += copy[i+1][j].rgbtGreen;
                sum_blue += copy[i+1][j].rgbtBlue;
                counter++;
            }

            if ((i + 1 >= 0 && j - 1 >= 0) && (i + 1 < height && j - 1 >= 0))
            {
                sum_red += copy[i+1][j-1].rgbtRed;
                sum_green += copy[i+1][j-1].rgbtGreen;
                sum_blue += copy[i+1][j-1].rgbtBlue;
                counter++;
            }

            if ((i + 1 >= 0 && j + 1 >= 0) && (i + 1 < height && j + 1 < width))
            {
                sum_red += copy[i+1][j+1].rgbtRed;
                sum_green += copy[i+1][j+1].rgbtGreen;
                sum_blue += copy[i+1][j+1].rgbtBlue;
                counter++;
            }

            image[i][j].rgbtRed = round(sum_red / counter);
            image[i][j].rgbtGreen = round(sum_green / counter);
            image[i][j].rgbtBlue = round(sum_blue / counter);
        }
    }
    return;
}
