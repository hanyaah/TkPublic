#==================================================
#=================MOVE DICTIONARIES================
#==================================================

straightAxis = {'u': 'AP', 
                'd': 'DWN', 
                'b': 'BCK', 
                'f': 'FW',
                }

straightAxisFinal = {'AP': '<:UP:304165643282808833>', 
                     'DWN': '<:DOWN:304165435233009664>', 
                     'BCK': '<:BACK:304165586756304896>', 
                     'FW': '<:FORWARD:303930958049181719>'}

diagAxis = {'d/f': 'DFORWARD', 
            'u/f': 'AFORWARD', 
            'u/b': 'ABACKWARD', 
            'd/b': 'DBACKWARD',
            }               

diagAxisFinal = {'DFORWARD': '<:DOWNFORWARD:304165396217593856>', 
                 'AFORWARD': '<:UPFORWARD:304165667576479744>', 
                 'ABACKWARD': '<:UPBACK:304165623150149632>', 
                 'DBACKWARD': '<:DOWNBACK:304165565956620289>'}

nullAxis = {'n': 'NEWT'}

nullAxisFinal = {'NEWT': '<:NEUTRAL:304178841327239168>'}

multiAxis = {'qcf': 'QCFwD', 
             'qcb': 'QcBwD', 
             'hcf': 'HcFwD', 
             'hcb': 'HcBwD'}

multiAxisFinal = {'QCFwD': '<:DOWN:304165435233009664><:DOWNFORWARD:304165396217593856><:FORWARD:303930958049181719>', 
             'QcBwD': '<:DOWN:304165435233009664><:DOWNBACK:304165565956620289><:BACK:304165586756304896>', 
             'HcFwD': '<:BACK:304165586756304896><:DOWNBACK:304165565956620289><:DOWN:304165435233009664><:DOWNFORWARD:304165396217593856><:FORWARD:303930958049181719>', 
             'HcBwD': '<:FORWARD:303930958049181719><:DOWNFORWARD:304165396217593856><:DOWN:304165435233009664><:DOWNBACK:304165565956620289><:BACK:304165586756304896>'}

soloButton = {'1': 'LeP', 
              '2': 'RightP', 
              '3': 'LeK', 
              '4': 'RightK'}
#you left off here

soloButtonFinal = {'LeP': '<:1_:304166000369336321>', 
                   'RightP': '<:2_:304166127985098763>', 
                   'LeK': '<:3_:304166145299054592>', 
                   'RightK': '<:4_:304166174541742082>'}

duoButton = {'1+2': 'LpRpxx', 
             '2+3': 'RpLkxx', 
             '3+4':'LkRkxx', 
             '1+4': 'LpRkxx', 
             '1+3': 'LpLkxx', 
             '2+4':'RpRkxx'}

duoButtonFinal = {'LpRpxx': '<:12:304166229516746752>', 
                  'RpLkxx': '<:23:304166647571415053>', 
                  'LkRkxx':'<:34:304166275356295178>', 
                  'LpRkxx': '<:14:304166630185893888>', 
                  'LpLkxx': '<:13:304166304946847754>', 
                  'RpRkxx':'<:24:304166321992761344>'}

triButton = {'1+2+3': 'LpRpLk', 
             '1+2+4': 'LpRpRk', 
             '1+3+4': 'LpLkRk',
             '2+3+4': 'RpLkRk'}

quadButton ={'1+2+3+4': 'LpRpLkRk'}

#==================================================
#==============END MOVE DICTIONARIES===============
#==================================================

#==================================================
#====================STANCE LIST===================
#==================================================

#This took forever to write
stance = {'Vertical jump','Forward jump', 'DFLIP', 'Jump', 'TPORT', '(Hold)', '(Close)','When hit','in rage ','After stance ends', '(Cancel)'
          ,'Opponent Down', 'Grounded face up', 'DBT', 'DES', 'BAL', 'STB', 'FLY', 'HSP', 'RLX', 'MG', 'DWF', 'STC', 'KNP'
          ,'BT', 'GOL', 'SG', 'FC', 'RAI', 'HS', 'LFF', 'RFF', 'LFS', 'RFS', 'CSK', 'SIT', 'ZEN', 'CDS', 'SWS', 'SWB', 'HAR', 'DVK'
          ,'ALI', 'JGS', '(one spin)', '(two spins)', '(three spins)', '(four spins)', '(five spins)', '(Very long hold)', '(CH in front)'
          ,'When hit f', 'SEN', '(Opponent in air)', '(Close)', '(When hit )', '(to DSS)', 'DSS', 'RDS','DS', '(to TFS)', 'TFS-success', 'TFS-whiff '
          ,'(Hold as long as possible)', 'HMS', '(Hit in front)', 'MS', 'Sway', '(First hit only)', '(First hit whiffs)', '(Second hit only)','(Second hit miss)', 'KNK', 'BOK'
          ,'From certain moves', 'TWISTL', 'TWISTR', 'SCT', '(to HAZ)', 'HAZ', '(Second part)', 'SAV', '(Second hit ducked)'
          ,'(Only first hit on counter)','Tech (Far)', '(Far)', 'Tech', '(Crouching or far)', 'SNK', 'to Weave', 'When parry successful'
          ,'(to ALB)','ALB','Ext DCK','DCK', 'PAB','PKB', 'SWY','FLIK', '(After on step)', '(After two step)', '(After three step)', 'AOP', 'PDP'
          ,'(First stage)', '(Second stage)', 'KIN', 'MED', 'FLE', 'WFL', 'IND', 'INS', 'DGF', '(to NSS)', 'NSS', 'DEN'
         }
#==================================================
#=================END STANCE LIST==================
#==================================================