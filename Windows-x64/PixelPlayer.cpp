/*
MIT License

Copyright (c) 2022 ChenPi11

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.*/
// PixelPlayer.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include <opencv2/opencv.hpp>
#include <iostream>
#include <string>
#include <Windows.h>
#include <signal.h>
using namespace cv;
#ifndef STD_OUTPUT_HANDLE
#define STD_OUTPUT_HANDLE (DWORD)-11
#endif
#include <csignal>
#ifndef FORMAT_MESSAGE_FROM_SYSTEM
#define FORMAT_MESSAGE_FROM_SYSTEM     0x00001000
#endif 
COORD coordScreen = { 0, 0 };
HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);//获取标准输出句柄
#define ConsoleClear() SetConsoleCursorPosition(hConsole, coordScreen)
#define rgb(r,g,b,s) std::string("\x1b[38;2;")+std::to_string(r)+";"+std::to_string(g)+";"+std::to_string(b)+"m"+s
void cls()
{
	COORD coordScreen = { 0, 0 };
	DWORD cCharsWritten;
	DWORD dwConSize;
	HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);//获取标准输出句柄
	CONSOLE_SCREEN_BUFFER_INFO csbi;
	GetConsoleScreenBufferInfo(hConsole, &csbi);//获取标准输出句柄的屏幕缓冲区信息
	dwConSize = csbi.dwSize.X * csbi.dwSize.Y;
	FillConsoleOutputCharacterA(hConsole, ' ', dwConSize, coordScreen, &cCharsWritten);//填充标准输出句柄的屏幕缓冲区
	GetConsoleScreenBufferInfo(hConsole, &csbi);//获取标准输出句柄的屏幕缓冲区信息
	FillConsoleOutputAttribute(hConsole, csbi.wAttributes, dwConSize, coordScreen, &cCharsWritten);//填充标准输出句柄的屏幕缓冲区
	SetConsoleCursorPosition(hConsole, coordScreen);//设置标准输出句柄的光标位置
}
std::pair<int,int> get_terminal_size()
{
	CONSOLE_SCREEN_BUFFER_INFO csbi;
	GetConsoleScreenBufferInfo(hConsole, &csbi);
	return std::make_pair(csbi.srWindow.Right - csbi.srWindow.Left + 1, csbi.srWindow.Bottom - csbi.srWindow.Top + 1);
}
void printerror(DWORD e)
{
	LPVOID lpMsgBuf;
	FormatMessageA(
		FORMAT_MESSAGE_ALLOCATE_BUFFER |
		FORMAT_MESSAGE_FROM_SYSTEM |
		FORMAT_MESSAGE_IGNORE_INSERTS,
		NULL,
		e,
		MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
		(LPSTR)&lpMsgBuf,
		0,
		NULL
	);

	std::cout<<"PixelPlayer Error:" << (char*)lpMsgBuf;
	LocalFree(lpMsgBuf);
}
bool running;
void OnProgExit(int s) noexcept
{
	running = false;
}
int x,y;
int jmp = 0;
std::string file;
int main(int argc,char* argv[])
{
	try
	{
		//bind signal
		signal(SIGINT, OnProgExit);
		signal(SIGTERM, OnProgExit);
		signal(SIGABRT, OnProgExit);
		signal(SIGBREAK, OnProgExit);
		signal(SIGILL, OnProgExit);
		if (argc > 1)
		{
			if (strcmp(argv[1], "-h") == 0)
			{
				goto HLP;
			}
			else if (argc > 3)
			{
				if (strcmp(argv[2], "-j") == 0)
				{
					jmp = std::atoi(argv[3]);
				}
			}
			file=argv[1];
		}
		else
		{
			HLP:
			std::cout << "Usage: PixelPlayer.exe <video file> [-j <jump>] | -h" << std::endl;
			std::cout << "\t -h        Help" << std::endl;
			std::cout << "\t -j <jump> Jump frame" << std::endl;
			return 0;
		}
		auto cap = VideoCapture(file);
		if (!cap.isOpened())
		{
			printerror(GetLastError());
			return -1;
		}
		//int fps = cap.get(CAP_PROP_FPS);
		running = true;
		unsigned long long i = 0;
		while (running)
		{
			for (int i = 0; i < jmp; i++)
			{
				Mat f;
				cap >> f;
				f.release();
			}
			Mat frame;
			cap >> frame;
			if (frame.empty())
			{
				break;
			}
			x = get_terminal_size().first;
			y = get_terminal_size().second;
			Mat fme;
			resize(frame, fme, Size(x / 2, y - 1));//由于一个完整方块是高宽2:1,所以1像素2方块，x/2。最后的\n可能会使画面抖动，所以去掉最后一行(y-1)
			ConsoleClear();
			for (int i = 0; i < (y - 1); i++)
			{
				for (int j = 0; j < x / 2; j++)
				{
					int r = fme.at<Vec3b>(i, j)[2];
					int g = fme.at<Vec3b>(i, j)[1];
					int b = fme.at<Vec3b>(i, j)[0];
					std::cout << rgb(r, g, b, "██");
				}
				std::cout << std::endl;
			}
			fme.release();
			frame.release();
		}
		cap.release();
		SetConsoleTextAttribute(hConsole, 0x07);
		std::exit(0);
		return 0;
	}
	catch (std::exception e)
	{
		cls();
		std::cout <<"Error:" << e.what()<<std::endl;
		return -1;
	}
	catch (...)
	{
		cls();
		std::cout << "Error" << std::endl;
		return -1;
	}
}
