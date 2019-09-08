#include "headers.h"

extern vector<string> file_name;
extern vector<string> file_perm;
extern vector<string> file_size;
extern vector<string> mod_date;
extern vector<string> gp_name;

std::vector<string>::iterator it;

  int cursor_move()
   {


     char ch, PATH[100], fix[100], pwd[100], enter[100], dirc[10], cwd[100], entry_file[100], my_buffer[100], back_sp[100] ;
     int size, cursor=0;

     vector<string> forward;
     vector<string> backward;

     enableRawMode();  // Enable Non-canonical mode

     // Setting the pointer
     printf("\033[10;4H \033[1;0;29m => ");
     int count=10;

     // Getting default current working directory
     getcwd(fix, sizeof(fix));

     // Default Home Screen
     list(fix);
     store_vectors(fix,cursor);
     current_wor_dir(fix);
     // Cursor Movement
     while(1)
      {
        printf("\033[4;180H \033[1;5;36m NORMAL MODE ");
        printf("\033[55;150H");
        fflush(stdin);
        ch=std::cin.get();
        strcpy(dirc,file_perm[cursor].c_str());

        if (ch == '\033')
         { // if the first value is esc

           std::cin.get(); // skip the [

           switch(std::cin.get())
            { // the real value


                case 'A':
                    // code for arrow up
                    size=file_name.size();

                    if(count>10 && cursor>0)
                    {
                        printf("\033[2J");
                        count--;
                        cursor--;

                        //Print After updation
                        list(fix);
                        store_vectors(fix,cursor);
                        current_wor_dir(fix);

                        strcpy(dirc,file_perm[cursor].c_str());
                        printf("\033[10;4H \033[1;0;29m %d=>%c ",cursor,dirc[0]);

                    }

                    else
                    {
                      printf("\033[2J");
                      count=size+9;
                      cursor=size-1;

                      //print after updation
                      list(fix);
                      store_vectors(fix,cursor);
                      current_wor_dir(fix);

                      strcpy(dirc,file_perm[cursor].c_str());
                      printf("\033[10;4H \033[1;0;29m %d=>%c ",cursor,dirc[0]);

                    }

                    break;




                 case 'B':
                    // code for arrow down
                    size=file_name.size();

                    if(count<size+9 && cursor<size)
                    {
                      printf("\033[2J");
                      count++;
                      cursor++;

                      //Print After updation

                      list(fix);
                      store_vectors(fix,cursor);
                      current_wor_dir(fix);

                      strcpy(dirc,file_perm[cursor].c_str());
                      printf("\033[10;4H \033[1;0;29m %d=>%c ",cursor,dirc[0]);

                    }

                    else
                    {
                      printf("\033[2J");

                      count=10;
                      cursor=0;

                      //Print after updation

                      list(fix);
                      store_vectors(fix,cursor);
                      current_wor_dir(fix);

                      strcpy(dirc,file_perm[cursor].c_str());
                      printf("\033[10;4H \033[1;0;29m %d=>%c ",cursor,dirc[0]);

                    }
                    break;



                  case 'C':
                      // code for arrow right


                      if(!forward.empty())
                      {
                        string sm;
                        // popping the address from where I have come
                        sm=forward.back();
                        forward.pop_back();
                        strcpy(enter,sm.c_str());  // As Enter variable is availaible


                        backward.push_back(fix);
                        printf("\033[2J");  // Clear Screen


                        // Restore Screen
                        cursor=0;
                        count=10;
                        printf("\033[10;4H \033[1;0;29m %d=> ",cursor);

                        //Print after updation
                        list(enter);
                        store_vectors(enter,cursor);

                        strcpy(fix,enter);
                        current_wor_dir(fix);

                        strcpy(dirc,file_perm[cursor].c_str());
                        printf("\033[10;4H %d=>%c ",cursor,dirc[0]);

                      }

                      else
                      {
                            printf("\033[2;150H \033[0;1;31m Sorry, Not allowed , Stacks Empty!!!!!");
                      }

                      break;




                  case 'D':
                      // code for arrow left

                      if(backward.empty()){
                          printf("\033[2;150H \033[0;1;31m Sorry, It is not Possible !! Stack is empty!!!!");
                        }


                      else{
                          // popping the address from where I have come
                            string sn;
                          sn=backward.back();
                          backward.pop_back();
                          strcpy(enter,sn.c_str());



                          forward.push_back(fix);
                          printf("\033[2J");  // Clear Screen



                          //Restore Screen
                          count=10;
                          cursor=0;
                          printf("\033[10;4H \033[1;0;29m %d=> ",cursor);
                          //Print after updation
                          list(enter);
                          store_vectors(enter,cursor);

                          strcpy(fix,enter);
                          current_wor_dir(fix);


                          strcpy(dirc,file_perm[cursor].c_str());
                          printf("\033[10;4H %d=>%c ",cursor,dirc[0]);
                         }
                      break;

              }
            }



    //********code for enter*****************


          if(ch=='\n')
           {
             if(dirc[0]=='d')
             {

             // CONCATENATION
             strcpy(enter,fix);
             backward.push_back(enter);     // pushing vector

             // Path Formation
             strcat(enter,"/");
             strcpy(PATH,file_name[cursor].c_str());
             strcat(enter,PATH);


             printf("\033[2J");  // Clear Screen


             // Important condition check
             it = find(forward.begin(), forward.end(), enter);

              if (it != forward.end() )
              {
                //element present
              string sn;
              sn=forward.back();
              forward.pop_back();
              strcpy(enter, sn.c_str());
              }

              else{
                forward.clear();

              }


             // Restore Screen
             count=10;
             cursor=0;

             // Printing Function and Intialization
             list(enter);
             store_vectors(enter,cursor);


             strcpy(fix,enter);
             current_wor_dir(fix);

             strcpy(dirc,file_perm[cursor].c_str());
             printf("\033[10;4H %d=>%c ",cursor,dirc[0]);

           }


          //Opening file in gedit
           else if(dirc[0] != 'd')
           {
              printf("\033[2J");
             list(fix);
             store_vectors(fix,cursor);
             // entry to file
             strcpy(entry_file,"xdg-open ");
             strcat(entry_file,file_name[cursor].c_str());
             strcat(entry_file,">log.txt");
             system(entry_file);

           }


         }


         // CODE for BACK space
         if(ch==127)
         {

           //Popping the backward

           if(!backward.empty())
              {
                 string sn;
                 sn=backward.back();
                 backward.pop_back();
                 strcpy(back_sp,sn.c_str());


                 // Pushing.....Forming the pwd PATH which is used to push in the vector
                 strcpy(pwd,fix);        //Taking value from our common buffer
                 strcat(pwd,"/");
                 strcpy(PATH,file_name[cursor].c_str());
                 strcat(pwd,PATH);
                 forward.push_back(pwd);
                 printf("\033[2J");  // Clear Screen

                 //Restore Screen
                 count=10;
                 cursor=0;
                 printf("\033[10;4H \033[1;0;29m %d=> ",cursor);
                 //Print after updation

                 list(back_sp);
                 store_vectors(back_sp,cursor);

                 strcpy(fix,back_sp);

                 current_wor_dir(fix);
               }

               else
               {
                 printf("\033[3;50H \033[0;1;31m  !! Stack is empty!!!!") ;

               }


         }



         // Handling Home Button
           if(ch=='h'||ch=='H'){
             getcwd(cwd, sizeof(cwd));
             count=10;
             cursor=0;

             list(cwd);
             store_vectors(cwd,cursor);


             strcpy(fix,cwd);
             current_wor_dir(fix);
           }




        // Entering to command mode
        if(ch==':')
         {

              label1:     // Restore command mode After typing Command
              int i=26;
              int j=0;
              char ch1='a';
              printf("\033[4;180H \033[1;5;31m COMMAND MODE ");
              printf("\033[50;3H \033[1;0;38m Type Your command :");
              printf("\033[50;%dH",i+j);


                while(1)
                    {

                          if(ch1=='\n')    // ON ENTER
                          {
                             char fix_new[100];
                             strcpy(fix_new,fix); // Not taking risk for fix

                              my_buffer[j]='\0'; // Setting Null to my buffer
                              printf("\e[2K]");
                              process_command(my_buffer,fix_new);
                              goto label1;
                          }

                        else if(ch1=='\033')    // ON ENTER
                          {
                            printf("\e[2K]");
                            break;
                          }



                          //storing to buffer and printing it
                          else
                          {
                            ch1=std::cin.get(); // To escape the 'a'


                              while(ch1!='\n' && j>=0) // Boundary Condition j>=0
                              {

                                      //Handling back spaces Boundary Condition j>0
                                      if(ch1==127 && j>0)
                                      {
                                        j--;
                                        printf("\033[50;%dH",i+j);
                                        printf("  ");
                                        printf("\033[50;%dH",i+j);
                                      }

                                      //Reading commands
                                      else
                                      {
                                        my_buffer[j] = ch1;
                                        printf("%c",my_buffer[j]);
                                        j++;
                                      }
                                      ch1=std::cin.get();  //  my_buffer[i]='\0';


                                      if(ch1=='\033')    // ON Escape Go OUT
                                        {
                                          printf("\e[2K]");
                                          break;
                                        }
                                }// end of while loop
                            }//else ends

                  }//While(1) ends here

           }// if ends here


        } // while(1) ends here



   return 0;
  }

