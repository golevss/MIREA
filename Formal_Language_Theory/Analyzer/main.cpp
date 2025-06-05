#include <iostream>
#include <fstream>
#include <cstring>
#include <string>
#include <vector>

typedef const char* lex_names;	// ВАР: 213321

enum state // Состояния конечного автомата
{
	S,      // Начальное состояние конечного автомата 
	ID,     // Обработка идентификаторов конечным автоматом
	NUM,    // Обработка чисел конечным автоматом
	COM,    // Обработка комментариев конечным автоматом
	EQ,     // Обработка операторов сравнивания и присвоения конечным автоматом
	NEQ,    // Обработка унарной операции или оператора неравенства конечным автоматом
	OP      // Обработка бинарных операций конечным автоматом
};
// Все лексемы
enum lex_types
{
	LEX_NULL,       // 0
	// Ключевые слова
	LEX_INT,        // 1
	LEX_FLOAT,      // 2
	LEX_BOOL,       // 3
	LEX_BEGIN,      // 4
	LEX_END,        // 5
	LEX_IF,         // 6
	LEX_ELSE,       // 7
	LEX_FOR,        // 8
	LEX_TO,         // 9
	LEX_STEP,       // 10
	LEX_NEXT,       // 11
	LEX_WHILE,      // 12
	LEX_READLN,     // 13
	LEX_WRITELN,    // 14
	LEX_TRUE,       // 15
	LEX_FALSE,      // 16
	LEX_PROGRAM,    // 17
	LEX_VAR,        // 18
	// Слова разделители
	LEX_SEMICOLON,  // 19
	LEX_COMMA,      // 20
	LEX_ASSIGN,     // 21
	LEX_EQ,         // 22
	LEX_NEQ,        // 23
	LEX_LSS,        // 24
	LEX_GTR,        // 25
	LEX_REQ,        // 26
	LEX_LEQ,        // 27
	LEX_PLUS,       // 28
	LEX_MINUS,      // 29
	LEX_OR,         // 30
	LEX_MULT,       // 31
	LEX_DIV,        // 32
	LEX_AND,        // 33
	LEX_NOT,        // 34
	LEX_START_COM,  // 35
	LEX_FINISH_COM, // 36
	LEX_LPAREN,     // 37
	LEX_RPAREN,     // 38
	// Общие слова
	LEX_NUM,        // 39
	LEX_ID          // 40
};
// Все лексемы в текстовом представлении
static lex_names lex_dec[] = {
	"LEX_NULL",
	"LEX_INT",
	"LEX_FLOAT",
	"LEX_BOOL",
	"LEX_BEGIN",
	"LEX_END",
	"LEX_IF",
	"LEX_ELSE",
	"LEX_FOR",
	"LEX_TO",
	"LEX_STEP",
	"LEX_NEXT",
	"LEX_WHILE",
	"LEX_READLN",
	"LEX_WRITELN",
	"LEX_TRUE",
	"LEX_FALSE",
	"LEX_PROGRAM",
	"LEX_VAR",
	"LEX_SEMICOLON",
	"LEX_COMMA",
	"LEX_ASSIGN",
	"LEX_EQ",
	"LEX_NEQ",
	"LEX_LSS",
	"LEX_GTR",
	"LEX_REQ",
	"LEX_LEQ",
	"LEX_PLUS",
	"LEX_MINUS",
	"LEX_OR",
	"LEX_MULT",
	"LEX_DIV",
	"LEX_AND",
	"LEX_NOT",
	"LEX_START_COM",
	"LEX_FINISH_COM",
	"LEX_LPAREN",
	"LEX_RPAREN",
	"LEX_NUM",
	"LEX_ID"
};
// Ключевык слова
static lex_names key_words[] = {
	"",
	"int",
	"float",
	"bool",
	"begin",
	"end",
	"if",
	"else",
	"for",
	"to",
	"step",
	"next",
	"while",
	"readln",
	"writeln",
	"true",
	"false",
	"program",
	"var",
	NULL
};
// Лексемы ключевых слов
static lex_types type_key_words[] = {
	LEX_NULL,
	LEX_INT,
	LEX_FLOAT,
	LEX_BOOL,
	LEX_BEGIN,
	LEX_END,
	LEX_IF,
	LEX_ELSE,
	LEX_FOR,
	LEX_TO,
	LEX_STEP,
	LEX_NEXT,
	LEX_WHILE,
	LEX_READLN,
	LEX_WRITELN,
	LEX_TRUE,
	LEX_FALSE,
	LEX_PROGRAM,
	LEX_VAR,
	LEX_NULL
};
// Разделители
static lex_names sep_words[] = {
	"",
	";",
	",",
	":=",
	"==",
	"!=",
	">",
	"<",
	">=",
	"<=",
	"+",
	"-",
	"||",
	"*",
	"/",
	"&&",
	"!",
	"{",
	"}",
	"(",
	")",
	NULL
};
// Лексемы разделитей
static lex_types type_sep_words[] = {
	LEX_NULL,
	LEX_SEMICOLON,
	LEX_COMMA,
	LEX_ASSIGN,
	LEX_EQ,
	LEX_NEQ,
	LEX_LSS,
	LEX_GTR,
	LEX_REQ,
	LEX_LEQ,
	LEX_PLUS,
	LEX_MINUS,
	LEX_OR,
	LEX_MULT,
	LEX_DIV,
	LEX_AND,
	LEX_NOT,
	LEX_START_COM,
	LEX_FINISH_COM,
	LEX_LPAREN,
	LEX_RPAREN,
	LEX_NULL
};

// Структура токена
struct token
{
	lex_types type;     // Тип токена
	std::string value;  // Значение токена
	size_t x_coord = 0; // Номер позиции
	size_t y_coord = 0; // Номер строки
};
// ========== Лексер ==========
struct lex 
{
	std::vector<token> tokensVec;   // Поле хранящee все токены
	std::string inputString = "";   // Поле хранящее считываемую строку
	size_t x_coord = 0;             // Поле хранящее номер считываемой строки
	size_t y_coord = 0;             // Поле хранящее номер считываемого символа
	char c = 0;                     // Поле хранящее анализируемый символ
	std::string lexBuff = "";       // Поле хранящее анализируемую лексему
	state cState = S;               // Поле хранящее состояние конечного автомата
	token buffToken;                // Поле хранящее анализируемый токен
	// Входной буфер
	lex(const char* fileName)
	{
		std::ifstream inputFile(fileName);
		while (getline(inputFile,inputString))
		{
			y_coord++;
			reading_mechanism(inputString);
		}
		proc_tokens();
	}
	// Считывающая машина представляющая собой конечный автомат
	void reading_mechanism(std::string inputString)
	{
		for (size_t i = 0; i < inputString.size(); i++)
		{
			c = inputString[i];
			switch (cState)
			{
			case S:
				if (c == ' ' || c == '\n' || c == '\t' || c == '\r')
					cState = S;
				else if (isalpha(c))
				{
					clear_string();
					x_coord = i + 1;
					add_to_string();
					cState = ID;
				}
				else if (isdigit(c) || c =='.')
				{
					clear_string();
					x_coord = i + 1;
					add_to_string();
					cState = NUM;
				}
				else if (c == '{')
				{
					clear_string();
					x_coord = i + 1;
					add_to_string();
					cState = COM;
				}
				else if (c == ':' || c == '>' || c == '<' || c == '=')
				{
					clear_string();
					x_coord = i + 1;
					add_to_string();
					cState = EQ;
				}
				else if (c == '!')
				{
					clear_string();
					x_coord = i + 1;
					cState = NEQ;
					add_to_string();
				}
				else if (c == '+' || c == '-' || c == '|' || c == '*' || c == '/' || c == '&')
				{
					clear_string();
					x_coord = i + 1;
					add_to_string();
					cState = OP;
				}
				else
				{
					if (key_lex() || sep_lex() || num_lex() || id_lex())
					{
						clear_string();
						x_coord = i + 1;
						add_to_string();
					}
					else
					{
						std::cerr << "ERROR (inncorrect symbol) -> " << c << " (" << x_coord << ',' << i++ << ')' << std::endl;
						exit(101);
					}
				}
				break;
			case NUM:
				if (((c == '+' || c == '-') && tolower(inputString[i-1]) == 'e') || isalpha(c) || isdigit(c) || c == '.')
					add_to_string();
				else
				{
					i--;
					cState = S;
				}
				break;
			case ID:
				if (isalpha(c) || isdigit(c))
					add_to_string();
				else
				{
					i--;
					cState = S;
				}
				break;
			case COM:
				if (c == '}')
				{
					add_to_string();
					lexBuff = "";
					cState = S;
				}
				else
					add_to_string();
				break;
			case EQ:
				if (c == '=')
				{
					add_to_string();
					cState = S;
				}
				else if (sep_lex())
				{
					std::cerr << "ERROR (incorrect comparison opperator) -> " << lexBuff << " (" << y_coord << ',' << x_coord << ')' << std::endl;
					exit(103);
				}
				else if (lexBuff.size() == 1 && (lexBuff != ">" && lexBuff != "<"))
				{
					std::cerr << "ERROR (incorrect opperator) -> " << lexBuff << " (" << y_coord << ',' << x_coord << ')' << std::endl;
					exit(104);
				}
				else
				{
					i--;
					cState = S;
				}
				break;
			case NEQ:
				if (c == '=')
				{
					add_to_string();
					cState = S;
				}
				else
				{
					i--;
					cState = S;
				}
				break;
			case OP:
				if ((c == '|' || c == '&') && lexBuff[0] == c)
				{
					add_to_string();
					cState = S;
				}
				else if ((c == '|' || c == '&') && lexBuff[0] != c)
				{
					std::cerr << "ERROR (incorrect logical opperator) -> " << lexBuff << " (" << y_coord << ',' << x_coord << ')' << std::endl;
					exit(105);
				}
				else
				{
					i--;
					cState = S;
				}
				break;
			default:
				break;
			}
		}
		clear_string();
	}
	// Метода добавления символа в лексему
	void add_to_string() {lexBuff += c;}
	// Метод анализа лексемы
	void clear_string()
	{
		buffToken.value = lexBuff;
		buffToken.x_coord = x_coord;
		buffToken.y_coord = y_coord;
		lexBuff = "";
		if (key_lex() || sep_lex() || num_lex() || id_lex())
			tokensVec.push_back(buffToken);
		else
		{
			std::cerr << "ERROR (incorrect input) -> " << buffToken.value << " (" << y_coord << ',' << x_coord << ')' << std::endl;
			exit(102);
		}
	}
	// Метод проверки на ключевые слова
	bool key_lex()
	{
		int i = 0;
		while (key_words[i] != NULL)
		{
			if (buffToken.value == key_words[i])
			{
				buffToken.type = type_key_words[i];
				return true;
			}
			i++;
		}
		return false;
	}
	// Метод проверки на разделительные слова
	bool sep_lex()
	{
		int i = 0;
		while (sep_words[i] != NULL)
		{
			if (buffToken.value == sep_words[i])
			{
				buffToken.type = type_sep_words[i];
				return true;
			}
			i++;
		}
		return false;
	}
	// Метод проверки на число
	bool num_lex()
	{
		char lastSymb = tolower(buffToken.value[buffToken.value.size() - 1]);
		if (isdigit(buffToken.value[0]) || buffToken.value[0] == '.')
			if (isalpha(lastSymb))
				if (lastSymb == 'b' || lastSymb == 'o' || lastSymb == 'd' || lastSymb == 'h')
				{
					buffToken.type = LEX_NUM;
						return true;
				}
				else
				{
					return false;
				}
			else if (check_e(buffToken.value))
				{
					buffToken.type = LEX_NUM;
					return true;
				}
		
		return false;
	}
	// Метод проверки на идентификаторв
	bool id_lex()
	{
		if (isalpha(buffToken.value[0]))
		{
			buffToken.type = LEX_ID;
			return true;
		}
		return false;
	}
	// МЕтод проверки действительного числа
	bool check_e(std::string buffStr)
	{
		size_t ePlace = -1;
		size_t dPlace = -1;
		if (buffStr[buffStr.size() - 1] == '.' || buffStr[buffStr.size() - 1] == '+' || buffStr[buffStr.size() - 1] == '-')
			return false;
		for (size_t i = 0; i < buffStr.size(); i++)
		{
			if (tolower(buffStr[i]) == 'e' && ePlace == -1)
			{
				if (dPlace != -1 && dPlace == i - 1)
					return false;
				ePlace = i;
			}
			else if (buffStr[i] == '.' && dPlace == -1)
			{
				if (ePlace != -1)
					return false;
				dPlace = i;
			}
			else if ((dPlace == i - 1 && (isalpha(buffStr[i]))) || ((buffStr[i] == '+' || buffStr[i] == '-') && ePlace != i - 1)
				|| (buffStr[i] == '.' && ((dPlace != -1 && dPlace != i) || ePlace != -1)) || (tolower(buffStr[i]) == 'e' && ((ePlace != -1 && ePlace != i))))
			{
				return false;
			}
		}
		if (ePlace != -1 && buffStr[ePlace+1] != '+' && buffStr[ePlace+1] != '-')
			return false;
		return true;
	}
	// Метод вывода всех токенов на экран
	void print_all_tokens()
	{
		for (auto el = tokensVec.begin(); el != tokensVec.end(); el++)
			std::cout << '(' << lex_dec[el->type] << ')' << " -> " << el->value
			 /* << " (" << el->x_coord << ';' << el->y_coord << ')' */
			<< std::endl;
	}
	// Метод удаления пустых лексем
	void proc_tokens()
	{
		for (auto el = tokensVec.begin(); el != tokensVec.end(); )
			if (el->type == 0) el = tokensVec.erase(el);
			else el++;
	}
};
// Структура токена переменной
struct varTokens 
{
	std::string varType = "";
	std::string varName = "";
};
// ==========  Парсер  ==========
struct parser 
{
	size_t idx = 0;						// Поле хранящее индекс обрабатываемого токена
	size_t tokenCount = 0;				// Поле хранящее количество всех токенов
	std::vector <token> tokensVec;		// Поле хранящее все токены
	std::vector <varTokens> tokensVar;	// Поле хранящее все переменные
	varTokens singleTokenVar;			// Поле хранящее обрабатываемую переменную
	
	int ifWhileCheck = 0;
	bool ifWhileFlag = false;

	// Конструктор парсера
	parser(std::vector <token> tokensVec)
	{
		idx = 0;
		if (tokensVec[idx].type != LEX_PROGRAM)
		{
			std::cerr << "ERROR (there must be a keyword 'program') -> " << tokensVec[idx].value << " (" << tokensVec[idx].x_coord << ';' << tokensVec[idx].y_coord << ')' << std::endl;
			exit(201);
		}
		this->tokensVec = tokensVec;
		this->tokenCount = tokensVec.size();
		idx++;
	}
	// Запуск парсера
	void start_prog()
	{
		if (tokensVec[idx].type == LEX_VAR)
		{
			idx++;
			start_vars();
		}
		if (tokensVec[idx].type == LEX_BEGIN)
		{
			start_begin();
		}
		else
		{
			std::cerr << "ERROR (the program structure is broken) -> " << tokensVec[idx].value << " (" << tokensVec[idx].x_coord << ';' << tokensVec[idx].y_coord << ')' << std::endl;
			exit(202);
		}
	}
	// Метод обработки головы программы
	void start_vars()
	{
		switch (tokensVec[idx].type)
		{
		case LEX_INT:
			singleTokenVar.varType = "INT";
			idx++;
			break;
		case LEX_FLOAT:
			singleTokenVar.varType = "FLOAT";
			idx++;
			break;
		case LEX_BOOL:
			singleTokenVar.varType = "BOOL";
			idx++;
			break;
		default:
			std::cerr << "ERROR (there must be a type of variable) -> " << tokensVec[idx].value << " (" << tokensVec[idx].x_coord << ';' << tokensVec[idx].y_coord << ')' << std::endl;
			exit(203);
		}
		start_id();
		tokensVar.push_back(singleTokenVar);
		while (tokensVec[idx].type == LEX_COMMA)
		{
			idx++;
			for (int i = 0; i < tokensVar.size(); i++)
			{
				if (tokensVar[i].varName == tokensVec[idx].value)
				{
					std::cerr << "ERROR (re-declaring a variable) -> " << tokensVec[idx].value << " (" << tokensVec[idx].x_coord << ';' << tokensVec[idx].y_coord << ')' << std::endl;
					exit(222);
				}
			}
			start_id();
			tokensVar.push_back(singleTokenVar);
		}
	}
	// Метод проверки корректности переменной
	void start_id(bool flagToken = true)
	{
		if (tokensVec[idx].type == LEX_ID)
		{
			if (flagToken)
				singleTokenVar.varName = tokensVec[idx].value;
			else
				id_check();
			idx++;
		}
		else
		{
			std::cerr << "ERROR (there must be an id) -> " << tokensVec[idx].value << " (" << tokensVec[idx].x_coord << ';' << tokensVec[idx].y_coord << ')' << std::endl;
			exit(204);
		}
	}
	// Метод обработки тела программы
	void start_begin()
	{
		switch (tokensVec[idx].type)
		{
		case LEX_ID:
			id_check();
			idx++;
			if (tokensVec[idx].type == LEX_ASSIGN)
			{
				idx++;
				start_V();
			}
			else
			{
				std::cerr << "ERROR (there must be an assignment sign) -> " << tokensVec[idx].value << " (" << tokensVec[idx].x_coord << ';' << tokensVec[idx].y_coord << ')' << std::endl;
				exit(205);
			}
			break;
		case LEX_FOR:
			idx++;
			if (tokensVec[idx].type == LEX_ID)
			{
				id_check();
				idx++;
				if (tokensVec[idx].type == LEX_ASSIGN)
				{
					idx++;
					start_V();
					if (tokensVec[idx].type == LEX_TO)
					{
						idx++;
						start_V();
						if (tokensVec[idx].type == LEX_STEP)
						{
							idx++;
							start_V();
						}
						start_begin();
						if (tokensVec[idx].type == LEX_NEXT)
						{
							idx++;
							start_begin();
						}
						else
						{
							std::cerr << "ERROR (there must be a keyword 'next') -> " << tokensVec[idx].value << " (" << tokensVec[idx].x_coord << ';' << tokensVec[idx].y_coord << ')' << std::endl;
							exit(206);
						}
					}
					else
					{
						std::cerr << "ERROR (there must be a keyword 'to') -> " << tokensVec[idx].value << " (" << tokensVec[idx].x_coord << ';' << tokensVec[idx].y_coord << ')' << std::endl;
						exit(207);
					}
				}
				else
				{
					std::cerr << "ERROR (there must be an assignment sign) -> " << tokensVec[idx].value << " (" << tokensVec[idx].x_coord << ';' << tokensVec[idx].y_coord << ')' << std::endl;
					exit(208);
				}
			}
			else
			{
				std::cerr << "ERROR (there must be an ID) -> " << tokensVec[idx].value << " (" << tokensVec[idx].x_coord << ';' << tokensVec[idx].y_coord << ')' << std::endl;
				exit(209);
			}
			break;
		case LEX_IF:
			idx++;
			if (tokensVec[idx].type == LEX_LPAREN)
			{
				ifWhileCheck = idx - 1;
				idx++;
				ifWhileFlag = false;
				start_V();
				if (ifWhileFlag == false)
				{
					std::cerr << "ERROR ('if' statement accepts only logical expressions) -> " << tokensVec[ifWhileCheck].value << " (" << tokensVec[ifWhileCheck].x_coord << ';' << tokensVec[ifWhileCheck].y_coord << ')' << std::endl;
					exit(220);
				}
				if (tokensVec[idx].type == LEX_RPAREN)
				{
					idx++;
					start_begin();
					if (tokensVec[idx].type == LEX_ELSE)
					{
						idx++;
						start_begin();
					}
				}
				else
				{
					std::cerr << "ERROR (there must be an ')') -> " << tokensVec[idx].value << " (" << tokensVec[idx].x_coord << ';' << tokensVec[idx].y_coord << ')' << std::endl;
					exit(210);
				}
			}
			else
			{
				std::cerr << "ERROR (there must be an '(') -> " << tokensVec[idx].value << " (" << tokensVec[idx].x_coord << ';' << tokensVec[idx].y_coord << ')' << std::endl;
				exit(211);
			}
			break;
		case LEX_WHILE:
			idx++;
			if (tokensVec[idx].type == LEX_LPAREN)
			{
				ifWhileCheck = idx - 1;
				idx++;
				ifWhileFlag = false;
				start_V();
				if (ifWhileFlag == false)
				{
					std::cerr << "ERROR ('while' statement accepts only logical expressions) -> " << tokensVec[ifWhileCheck].value << " (" << tokensVec[ifWhileCheck].x_coord << ';' << tokensVec[ifWhileCheck].y_coord << ')' << std::endl;
					exit(221);
				}
				if (tokensVec[idx].type == LEX_RPAREN)
				{
					idx++;
					start_begin();
				}
				else
				{
					std::cerr << "ERROR (there must be an ')') -> " << tokensVec[idx].value << " (" << tokensVec[idx].x_coord << ';' << tokensVec[idx].y_coord << ')' << std::endl;
					exit(212);
				}
			}
			else
			{
				std::cerr << "ERROR (there must be an '(') -> " << tokensVec[idx].value << " (" << tokensVec[idx].x_coord << ';' << tokensVec[idx].y_coord << ')' << std::endl;
				exit(213);
			}
			break;
		case LEX_BEGIN:
			idx++;
			start_begin();
			while (tokensVec[idx].type == LEX_SEMICOLON)
			{
				idx++;
				start_begin();
			}
			if(tokensVec[idx].type == LEX_END)
			{
				idx++;
				break;
			}
			else
			{
				std::cerr << "ERROR (incorrect input) -> " << tokensVec[idx].value << " (" << tokensVec[idx].x_coord << ';' << tokensVec[idx].y_coord << ')' << std::endl;
				exit(214);
			}
			break;
		case LEX_READLN:
			idx++;
			start_id(false);
			while (tokensVec[idx].type == LEX_COMMA)
			{
				idx++;
				start_id(false);
			}
			break;
		case LEX_WRITELN:
			idx++;
			start_V();
			while (tokensVec[idx].type == LEX_COMMA)
			{
				idx++;
				start_V();
			}
			break;
		case LEX_END:
			if (idx == tokenCount - 1)
				break;
			else
			{
				std::cerr << "ERROR (incorrect input) -> " << tokensVec[idx].value << " (" << tokensVec[idx].x_coord << ';' << tokensVec[idx].y_coord << ')' << std::endl;
				exit(215);
			}
		default:
			std::cerr << "ERROR (incorrect input) -> " << tokensVec[idx].value << " (" << tokensVec[idx].x_coord << ';' << tokensVec[idx].y_coord << ')' << std::endl;
			exit(216);
		}
	}
	// Метод обработки выражения
	void start_V()
	{
		start_O();
		while (tokensVec[idx].type == LEX_EQ || tokensVec[idx].type == LEX_NEQ || tokensVec[idx].type == LEX_LSS
			|| tokensVec[idx].type == LEX_GTR || tokensVec[idx].type == LEX_REQ || tokensVec[idx].type == LEX_LEQ)
		{
			ifWhileFlag = true;
			idx++;
			start_O();
		}
	}
	// Метод обработки операнда
	void start_O()
	{
		start_S();
		while (tokensVec[idx].type == LEX_PLUS || tokensVec[idx].type == LEX_MINUS || tokensVec[idx].type == LEX_OR)
		{
			idx++;
			start_S();
		}
	}
	// Метод обработки слагаемого
	void start_S()
	{
		start_M();
		while (tokensVec[idx].type == LEX_MULT || tokensVec[idx].type == LEX_DIV || tokensVec[idx].type == LEX_AND)
		{
			idx++;
			start_M();
		}
	}
	// Метод обработки множителя
	void start_M()
	{
		if (tokensVec[idx].type == LEX_ID)
		{	
			if (tokensVar[0].varType == "BOOL") ifWhileFlag = true;
			id_check();
			idx++;
		}
		else if(tokensVec[idx].type == LEX_TRUE || tokensVec[idx].type == LEX_FALSE)
		{
			ifWhileFlag = true;
			idx++;
		}
		else if (tokensVec[idx].type == LEX_NUM)
		{
			num_check();
			idx++;
		}
		else if (tokensVec[idx].type == LEX_NOT)
		{
			idx++;
			start_M();
		}
		else if (tokensVec[idx].type == LEX_LPAREN)
		{
			idx++;
			if (tokensVec[idx].type == LEX_RPAREN)
				idx++;
		}
		else
		{
			std::cerr << "ERROR (there must be a variable or number) -> " << tokensVec[idx].value << " (" << tokensVec[idx].x_coord << ';' << tokensVec[idx].y_coord << ')' << std::endl;
			exit(217);
		}
	}
	// Метод проверяющий корректность введённого числа числа
	void num_check()
	{
		std::string str = tokensVec[idx].value;
		char maxS = 0;
		size_t fE = std::max(str.find('E'), str.find('e'));
		for (int i = 0; i < str.size() - 1; i++) maxS = std::max(maxS, str[i]);
		if ((tolower(str[str.size() - 1]) == 'b' && maxS > 49) || (tolower(str[str.size() - 1]) == 'o' && maxS > 55)
		|| (tolower(str[str.size() - 1]) == 'd' && maxS > 57) || ((fE < std::string::npos) && !(maxS > 47 && 58 > maxS)))
		{
			std::cerr << "ERROR (incorrect number) -> " << tokensVec[idx].value << " (" << tokensVec[idx].x_coord << ';' << tokensVec[idx].y_coord << ')' << std::endl;
			exit(218);
		}
	}
	// Метод проверяющий объявлена ли переменная
	void id_check()
	{
		for (int i = 0; i < tokensVar.size(); i++)
		{
			if (tokensVar[i].varName == tokensVec[idx].value)
				return;
		}
		std::cerr << "ERROR (undeclared or incorrect variable) -> " << tokensVec[idx].value << " (" << tokensVec[idx].x_coord << ';' << tokensVec[idx].y_coord << ')' << std::endl;
		exit(219);
	}
};

int main()
{
	const char* inputFileName = "input_file.txt";
	lex lexAnalys(inputFileName);
	lexAnalys.print_all_tokens(); // Вывод лексем

	// parser syntAnalys(lexAnalys.tokensVec);
	// syntAnalys.start_prog();

	std::cout << "CORRECT" << std::endl;
	return 0;
}