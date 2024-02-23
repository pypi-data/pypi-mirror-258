from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.db import *
import random
from colored import Style,Fore
class TasksMode:
    def display_field(self,fieldname):
        color1=Fore.rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        color2=Fore.rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        color3=Fore.rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        color4=Fore.rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        m=f"Item Num -|- BrCd -|- Cd -|- {fieldname}"
        hr='-'*len(m)
        print(f"{m}\n{hr}")
        if fieldname in self.valid_fields:
            with Session(self.engine) as session:
                results=session.query(Entry).filter(Entry.InList==True).all()
                if len(results) < 1:
                    print(f"{Fore.red}{Style.bold}Nothing is in List!{Style.reset}")
                for num,result in enumerate(results):
                    print(f"{Fore.red}{num}{Style.reset} -> {color1}{result.Name}{Style.reset}|{color2}{result.Barcode}{Style.reset}|{color3}{result.Code}{Style.reset}|{color4}{getattr(result,fieldname)}{Style.reset}")
        print(f"{m}\n{hr}")

    def setFieldInList(self,fieldname):
        while True:
            m=f"Item Num -|- BrCd -|- Cd -|- {fieldname}"
            hr='-'*len(m)
            print(f"{m}\n{hr}")
            if fieldname in self.valid_fields:
                with Session(self.engine) as session:
                    code=''
                    while True:
                        code=input("barcode|code: ")
                        if code in self.options['1']['cmds']:
                            self.options['1']['exec']()
                        elif code in self.options['2']['cmds']:
                            return
                        else:
                            break
                    value=0
                    while True:
                        value=input("amount|+amount|-amount: ")
                        if value in self.options['1']['cmds']:
                            self.options['1']['exec']()
                        elif value in self.options['2']['cmds']:
                            return
                        else:
                            try:
                                color1=Fore.rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255))
                                color2=Fore.rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255))
                                color3=Fore.rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255))
                                color4=Fore.rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255))
                                if value.startswith("-") or value.startswith("+"):
                                    value=float(value)
                                    result=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Code==code)).first()
                                    if result:
                                        setattr(result,fieldname,getattr(result,fieldname)+float(value))
                                        result.InList=True
                                        session.commit()
                                        session.flush()
                                        session.refresh(result)
                                        print(f"{color1}{result.Name}{Style.reset}|{color2}{result.Barcode}{Style.reset}|{color3}{result.Code}{Style.reset}|{color4}{getattr(result,fieldname)}{Style.reset}")
                                        print(f"{m}\n{hr}")

                                    else:
                                        raise Exception(result)
                                else:
                                    value=float(value)
                                    result=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Code==code)).first()
                                    if result:
                                        setattr(result,fieldname,value)
                                        result.InList=True
                                        session.commit()
                                        session.flush()
                                        session.refresh(result)
                                        print(f"{color1}{result.Name}{Style.reset}|{color2}{result.Barcode}{Style.reset}|{color3}{result.Code}{Style.reset}|{color4}{getattr(result,fieldname)}{Style.reset}")

                                        print(f"{m}\n{hr}")

                                    else:
                                        raise Exception(result)
                                break
                            except Exception as e:
                                print(e)

                    

    def __init__(self,engine):
        self.engine=engine
        self.valid_fields=['Shelf',
		'BackRoom',
		'Display_1',
		'Display_2',
		'Display_3',
		'Display_4',
		'Display_5',
		'Display_6',]
        #self.display_field("Shelf")
        self.options={
                '1':{
                    'cmds':['q','quit','#1'],
                    'desc':"quit program",
                    'exec':lambda: exit("user quit!"),
                    },
                '2':{
                    'cmds':['b','back','#2'],
                    'desc':'go back menu if any',
                    'exec':None
                    },
                }
        #autogenerate duplicate functionality for all valid fields for display
        count=3
        for entry in self.valid_fields:
            self.options[entry]={
                    'cmds':["#"+str(count),f"ls {entry}"],
                    'desc':f'list needed @ {entry}',
                    'exec':lambda self=self,entry=entry: self.display_field(f"{entry}"),
                    }
            count+=1
        #setoptions
        #self.setFieldInList("Shelf")
        for entry in self.valid_fields:
            self.options[entry+"_set"]={
                    'cmds':["#"+str(count),f"set {entry}"],
                    'desc':f'set needed @ {entry}',
                    'exec':lambda self=self,entry=entry: self.setFieldInList(f"{entry}"),
                    }
            count+=1

        while True:
            for option in self.options:
                print(f"{self.options[option]['cmds']} - {self.options[option]['desc']}")
            command=input("do what: ")
            for option in self.options:
                if self.options[option]['exec'] != None and command.lower() in self.options[option]['cmds']:
                    self.options[option]['exec']()
                elif self.options[option]['exec'] == None and command.lower() in self.options[option]['cmds']:
                    return


if __name__ == "__main__":
    TasksMode(engine=ENGINE)
