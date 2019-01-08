/PROG  SET_CUT_PARAMETRS
/ATTR
OWNER		= MNEDITOR;
COMMENT		= "ALX";
PROG_SIZE	= 52165;
CREATE		= DATE 16-05-13  TIME 14:56:20;
MODIFIED	= DATE 16-10-27  TIME 10:43:34;
FILE_NAME	= ;
VERSION		= 0;
LINE_COUNT	= 3832;
MEMORY_SIZE	= 54957;
PROTECT		= READ_WRITE;
TCD:  STACK_SIZE	= 0,
      TASK_PRIORITY	= 50,
      TIME_SLICE	= 0,
      BUSY_LAMP_OFF	= 0,
      ABORT_REQUEST	= 0,
      PAUSE_REQUEST	= 0;
DEFAULT_GROUP	= *,*,*,*,*;
CONTROL_CODE	= 00000000 00000000;
/APPL
  ARC Welding Equipment : 1,*,*,*,*;

MPAS %1;
MPAS_NUM_PASSES        : 0;
MPAS_LAST_PASS         : 0;
MPAS_CURRENT_PASS      : 0;
MPAS_STATUS_PASS       : 0;
/MN
1:  LBL[900] ;
2:  R[16:Parametr job]=AR[1]    ;
3:  R[17:Pirsing start]=AR[2]    ;
%pattern% %sn(4)%:\tIF R[16:Parametr job]=%cell(1, 4, 140)%,JMP LBL[%cell(1, 4, 140)%] ;
%pattern% %sn(144)%
/POS
/END
