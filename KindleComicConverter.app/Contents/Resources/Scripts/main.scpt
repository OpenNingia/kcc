FasdUAS 1.101.10   ��   ��    k             l      ��  ��   5/
# Copyright (c) 2012 Ciro Mattia Gonano <ciromattia@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for
# any purpose with or without fee is hereby granted, provided that the
# above copyright notice and this permission notice appear in all
# copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL
# WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
# AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL
# DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA
# OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
# TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.
#
# This script heavily relies on KindleStrip (C) by Paul Durrant and released in public domain
# 	(http://www.mobileread.com/forums/showthread.php?t=96903)
# Also, you need to have kindlegen v2.7 (with KF8 support) which is downloadable
# 	from Amazon website.
#
# Changelog:
#	1.0: first release
#	1.10: add CBZ/CBR support to comic2ebook.py
#	1.11: add CBZ/CBR support to KindleComicConverter
#	1.2: added image page splitting and optimizations
#
# Todo:
#	- bundle a script to manipulate images (to get rid of Mangle/E-nki/whatsoever)
     � 	 	
^ 
 #   C o p y r i g h t   ( c )   2 0 1 2   C i r o   M a t t i a   G o n a n o   < c i r o m a t t i a @ g m a i l . c o m > 
 # 
 #   P e r m i s s i o n   t o   u s e ,   c o p y ,   m o d i f y ,   a n d / o r   d i s t r i b u t e   t h i s   s o f t w a r e   f o r 
 #   a n y   p u r p o s e   w i t h   o r   w i t h o u t   f e e   i s   h e r e b y   g r a n t e d ,   p r o v i d e d   t h a t   t h e 
 #   a b o v e   c o p y r i g h t   n o t i c e   a n d   t h i s   p e r m i s s i o n   n o t i c e   a p p e a r   i n   a l l 
 #   c o p i e s . 
 # 
 #   T H E   S O F T W A R E   I S   P R O V I D E D   " A S   I S "   A N D   T H E   A U T H O R   D I S C L A I M S   A L L 
 #   W A R R A N T I E S   W I T H   R E G A R D   T O   T H I S   S O F T W A R E   I N C L U D I N G   A L L   I M P L I E D 
 #   W A R R A N T I E S   O F   M E R C H A N T A B I L I T Y   A N D   F I T N E S S .   I N   N O   E V E N T   S H A L L   T H E 
 #   A U T H O R   B E   L I A B L E   F O R   A N Y   S P E C I A L ,   D I R E C T ,   I N D I R E C T ,   O R   C O N S E Q U E N T I A L 
 #   D A M A G E S   O R   A N Y   D A M A G E S   W H A T S O E V E R   R E S U L T I N G   F R O M   L O S S   O F   U S E ,   D A T A 
 #   O R   P R O F I T S ,   W H E T H E R   I N   A N   A C T I O N   O F   C O N T R A C T ,   N E G L I G E N C E   O R   O T H E R 
 #   T O R T I O U S   A C T I O N ,   A R I S I N G   O U T   O F   O R   I N   C O N N E C T I O N   W I T H   T H E   U S E   O R 
 #   P E R F O R M A N C E   O F   T H I S   S O F T W A R E . 
 # 
 #   T h i s   s c r i p t   h e a v i l y   r e l i e s   o n   K i n d l e S t r i p   ( C )   b y   P a u l   D u r r a n t   a n d   r e l e a s e d   i n   p u b l i c   d o m a i n 
 #   	 ( h t t p : / / w w w . m o b i l e r e a d . c o m / f o r u m s / s h o w t h r e a d . p h p ? t = 9 6 9 0 3 ) 
 #   A l s o ,   y o u   n e e d   t o   h a v e   k i n d l e g e n   v 2 . 7   ( w i t h   K F 8   s u p p o r t )   w h i c h   i s   d o w n l o a d a b l e 
 #   	 f r o m   A m a z o n   w e b s i t e . 
 # 
 #   C h a n g e l o g : 
 # 	 1 . 0 :   f i r s t   r e l e a s e 
 # 	 1 . 1 0 :   a d d   C B Z / C B R   s u p p o r t   t o   c o m i c 2 e b o o k . p y 
 # 	 1 . 1 1 :   a d d   C B Z / C B R   s u p p o r t   t o   K i n d l e C o m i c C o n v e r t e r 
 # 	 1 . 2 :   a d d e d   i m a g e   p a g e   s p l i t t i n g   a n d   o p t i m i z a t i o n s 
 # 
 #   T o d o : 
 # 	 -   b u n d l e   a   s c r i p t   t o   m a n i p u l a t e   i m a g e s   ( t o   g e t   r i d   o f   M a n g l e / E - n k i / w h a t s o e v e r ) 
   
  
 l     ��������  ��  ��        p         ������ "0 comic2ebookpath comic2ebookPath��        p         ������ 0 kindlegenpath kindlegenPath��        p         ������ "0 kindlestrippath KindleStripPath��        p         ������ 0 thetitle TheTitle��        p         ������ 0 parentfolder ParentFolder��        l     ��������  ��  ��        i          I      �������� (0 getcomic2ebookpath GetComic2EbookPath��  ��     k     G ! !  " # " r      $ % $ n      & ' & 1    ��
�� 
psxp ' 4     �� (
�� 
file ( l    )���� ) b     * + * l   	 ,���� , I   	�� - .
�� .earsffdralis        afdr -  f     . �� /��
�� 
rtyp / m    ��
�� 
ctxt��  ��  ��   + m   	 
 0 0 � 1 1 B C o n t e n t s : R e s o u r c e s : c o m i c 2 e b o o k . p y��  ��   % o      ���� "0 comic2ebookpath comic2ebookPath #  2 3 2 r     4 5 4 m    ��
�� boovfals 5 o      ���� 0 
fileexists   3  6 7 6 O   + 8 9 8 Z   * : ;���� : I    �� <��
�� .coredoexbool        obj  < c     = > = o    ���� "0 comic2ebookpath comic2ebookPath > m    ��
�� 
psxf��   ; r   # & ? @ ? m   # $��
�� boovtrue @ o      ���� 0 
fileexists  ��  ��   9 m     A A�                                                                                  MACS  alis    t  Macintosh HD               �8�H+     N
Finder.app                                                      �S��        ����  	                CoreServices    �8҈      �͒       N   H   G  6Macintosh HD:System: Library: CoreServices: Finder.app   
 F i n d e r . a p p    M a c i n t o s h   H D  &System/Library/CoreServices/Finder.app  / ��   7  B C B Z   , D D E���� D l  , . F���� F H   , . G G o   , -���� 0 
fileexists  ��  ��   E I  1 @�� H I
�� .sysodlogaskr        TEXT H m   1 2 J J � K K v T h e   c o m i c 2 e b o o k   p y t h o n   s c r i p t   i s   m i s s i n g   f r o m   t h i s   p a c k a g e . I �� L M
�� 
appr L m   3 4 N N � O O ( K i n d l e C o m i c C o n v e r t e r M �� P Q
�� 
btns P J   5 8 R R  S�� S m   5 6 T T � U U  E x i t��   Q �� V��
�� 
dflt V m   9 :���� ��  ��  ��   C  W�� W L   E G X X o   E F���� 0 
fileexists  ��     Y Z Y l     ��������  ��  ��   Z  [ \ [ i     ] ^ ] I      �������� $0 getkindlegenpath GetKindlegenPath��  ��   ^ k     = _ _  ` a ` r      b c b n      d e d 1    ��
�� 
psxp e 4     �� f
�� 
file f l    g���� g m     h h � i i H M a c i n t o s h   H D : u s r : l o c a l : b i n : k i n d l e g e n��  ��   c o      ���� 0 kindlegenpath kindlegenPath a  j k j r   	  l m l m   	 
��
�� boovfals m o      ���� 0 
fileexists   k  n o n O   # p q p Z   " r s���� r I   �� t��
�� .coredoexbool        obj  t c     u v u o    ���� 0 kindlegenpath kindlegenPath v m    ��
�� 
psxf��   s r     w x w m    ��
�� boovtrue x o      ���� 0 
fileexists  ��  ��   q m     y y�                                                                                  MACS  alis    t  Macintosh HD               �8�H+     N
Finder.app                                                      �S��        ����  	                CoreServices    �8҈      �͒       N   H   G  6Macintosh HD:System: Library: CoreServices: Finder.app   
 F i n d e r . a p p    M a c i n t o s h   H D  &System/Library/CoreServices/Finder.app  / ��   o  z { z Z   $ : | }���� | l  $ & ~���� ~ H   $ &   o   $ %���� 0 
fileexists  ��  ��   } I  ) 6�� � �
�� .sysodlogaskr        TEXT � m   ) * � � � � � * K i n d l e g e n   i s   m i s s i n g . � �� � �
�� 
appr � m   + , � � � � � ( K i n d l e C o m i c C o n v e r t e r � �� � �
�� 
btns � J   - 0 � �  ��� � m   - . � � � � �  E x i t��   � �� ���
�� 
dflt � m   1 2���� ��  ��  ��   {  ��� � L   ; = � � o   ; <���� 0 
fileexists  ��   \  � � � l     ��������  ��  ��   �  � � � i     � � � I      �������� (0 getkindlestrippath GetKindleStripPath��  ��   � k     G � �  � � � r      � � � n      � � � 1    ��
�� 
psxp � 4     �� �
�� 
file � l    ����� � b     � � � l   	 ����� � I   	�� � �
�� .earsffdralis        afdr �  f     � �� ���
�� 
rtyp � m    ��
�� 
ctxt��  ��  ��   � m   	 
 � � � � � B C o n t e n t s : R e s o u r c e s : k i n d l e s t r i p . p y��  ��   � o      ���� "0 kindlestrippath KindleStripPath �  � � � r     � � � m    ��
�� boovfals � o      ���� 0 
fileexists   �  � � � O   + � � � Z   * � ����� � I    �� ���
�� .coredoexbool        obj  � c     � � � o    ���� "0 kindlestrippath KindleStripPath � m    ��
�� 
psxf��   � r   # & � � � m   # $��
�� boovtrue � o      ���� 0 
fileexists  ��  ��   � m     � ��                                                                                  MACS  alis    t  Macintosh HD               �8�H+     N
Finder.app                                                      �S��        ����  	                CoreServices    �8҈      �͒       N   H   G  6Macintosh HD:System: Library: CoreServices: Finder.app   
 F i n d e r . a p p    M a c i n t o s h   H D  &System/Library/CoreServices/Finder.app  / ��   �  � � � Z   , D � ����� � l  , . ����� � H   , . � � o   , -���� 0 
fileexists  ��  ��   � I  1 @�� � �
�� .sysodlogaskr        TEXT � m   1 2 � � � � � � T h e   k i n d l e s t r i p   p y t h o n   s c r i p t   i s   m i s s i n g   f r o m   t h i s   p a c k a g e .   P l e a s e   g e t   a   f r e s h   c o p y . � �� � �
�� 
appr � m   3 4 � � � � � ( K i n d l e C o m i c C o n v e r t e r � �� � �
�� 
btns � J   5 8 � �  ��� � m   5 6 � � � � �  E x i t��   � �� ��
�� 
dflt � m   9 :�~�~ �  ��  ��   �  ��} � L   E G � � o   E F�|�| 0 
fileexists  �}   �  � � � l     �{�z�y�{  �z  �y   �  � � � i     � � � I      �x�w�v�x (0 getexecutablepaths GetExecutablePaths�w  �v   � L      � � F      � � � F      � � � I     �u�t�s�u (0 getcomic2ebookpath GetComic2EbookPath�t  �s   � I    �r�q�p�r $0 getkindlegenpath GetKindlegenPath�q  �p   � I    �o�n�m�o (0 getkindlestrippath GetKindleStripPath�n  �m   �  � � � l     �l�k�j�l  �k  �j   �  � � � i     � � � I      �i ��h�i 0 comic2ebook Comic2Ebook �  ��g � o      �f�f 0 dir  �g  �h   � k     j � �  � � � r      � � � n      � � � 1    �e
�e 
psxp � o     �d�d 0 dir   � o      �c�c 0 dirpath dirPath �  � � � r     � � � b    	 � � � o    �b�b 0 parentfolder ParentFolder � m     � � � � � 0 K i n d l e C o m i c C o n v e r t e r . l o g � o      �a�a 0 resultsfile resultsFile �  � � � r     � � � b     � � � b     � � � b     � � � b     � � � b     � � � m     � � �    p y t h o n   � l   �`�_ n     1    �^
�^ 
strq o    �]�] "0 comic2ebookpath comic2ebookPath�`  �_   � m     � 
   K H D   � l   �\�[ n     1    �Z
�Z 
strq o    �Y�Y 0 dirpath dirPath�\  �[   � m    		 �

    � l   �X�W n     1    �V
�V 
strq o    �U�U 0 thetitle TheTitle�X  �W   � o      �T�T 0 shellcommand   �  Q     5 r   # * I  # (�S�R
�S .sysoexecTEXT���     TEXT o   # $�Q�Q 0 shellcommand  �R   o      �P�P 0 shellresult   R      �O
�O .ascrerr ****      � **** l     �N�M o      �L�L 0 error_message  �N  �M   �K�J
�K 
errn l     �I�H o      �G�G 0 error_number  �I  �H  �J   r   2 5 o   2 3�F�F 0 error_message   o      �E�E 0 shellresult    Z   6 g �D�C G   6 U!"! ?   6 A#$# l  6 ?%�B�A% I  6 ?�@�?&
�@ .sysooffslong    ��� null�?  & �>'(
�> 
psof' m   8 9)) �** 
 E r r o r( �=+�<
�= 
psin+ o   : ;�;�; 0 shellresult  �<  �B  �A  $ m   ? @�:�:  " ?   D Q,-, l  D O.�9�8. I  D O�7�6/
�7 .sysooffslong    ��� null�6  / �501
�5 
psof0 m   F I22 �33  W a r n i n g1 �44�3
�4 
psin4 o   J K�2�2 0 shellresult  �3  �9  �8  - m   O P�1�1    I  X c�056
�0 .sysodlogaskr        TEXT5 o   X Y�/�/ 0 shellresult  6 �.7�-
�. 
appr7 m   \ _88 �99 
 E r r o r�-  �D  �C   :�,: L   h j�+�+  �,   � ;<; l     �*�)�(�*  �)  �(  < =>= i    ?@? I      �'A�&�' 0 	kindlegen 	KindlegenA B�%B o      �$�$ 0 dir  �%  �&  @ k     `CC DED r     FGF b     HIH n     JKJ 1    �#
�# 
psxpK o     �"�" 0 dir  I m    LL �MM  / c o n t e n t . o p fG o      �!�! 0 opfpath opfPathE NON r    PQP b    RSR o    	� �  0 parentfolder ParentFolderS m   	 
TT �UU 0 K i n d l e C o m i c C o n v e r t e r . l o gQ o      �� 0 resultsfile resultsFileO VWV r    XYX b    Z[Z b    \]\ o    �� 0 kindlegenpath kindlegenPath] m    ^^ �__   [ l   `��` n    aba 1    �
� 
strqb o    �� 0 opfpath opfPath�  �  Y o      �� 0 shellcommand  W cdc Q    -efge r    "hih I    �j�
� .sysoexecTEXT���     TEXTj o    �� 0 shellcommand  �  i o      �� 0 shellresult  f R      �kl
� .ascrerr ****      � ****k l     m��m o      �� 0 error_message  �  �  l �n�
� 
errnn l     o��o o      �� 0 error_number  �  �  �  g r   * -pqp o   * +�� 0 error_message  q o      �
�
 0 shellresult  d rsr Z   . ]tu�	�t G   . Kvwv ?   . 9xyx l  . 7z��z I  . 7��{
� .sysooffslong    ��� null�  { �|}
� 
psof| m   0 1~~ � 
 E r r o r} ���
� 
psin� o   2 3� �  0 shellresult  �  �  �  y m   7 8����  w ?   < G��� l  < E������ I  < E�����
�� .sysooffslong    ��� null��  � ����
�� 
psof� m   > ?�� ���  W a r n i n g� �����
�� 
psin� o   @ A���� 0 shellresult  ��  ��  ��  � m   E F����  u I  N Y����
�� .sysodlogaskr        TEXT� o   N O���� 0 shellresult  � �����
�� 
appr� m   R U�� ��� 
 E r r o r��  �	  �  s ���� L   ^ `����  ��  > ��� l     ��������  ��  ��  � ��� i    ��� I      ������� 0 	stripfile 	StripFile� ���� o      ���� 0 dir  ��  ��  � k     ��� ��� r     ��� b     ��� n     ��� 1    ��
�� 
psxp� o     ���� 0 dir  � m    �� ���  / c o n t e n t . m o b i� o      ���� 0 origfilepath origFilePath� ��� r    ��� b    ��� b    ��� n    ��� 1   	 ��
�� 
psxp� o    	���� 0 parentfolder ParentFolder� o    ���� 0 thetitle TheTitle� m    �� ��� 
 . m o b i� o      ���� $0 strippedfilepath strippedFilePath� ��� r    ��� b    ��� o    ���� 0 parentfolder ParentFolder� m    �� ��� $ k i n d l e s t r i p l o g . t x t� o      ���� 0 resultsfile resultsFile� ��� r    +��� b    )��� b    %��� b    #��� b    ��� b    ��� m    �� ���  p y t h o n  � l   ������ n    ��� 1    ��
�� 
strq� o    ���� "0 kindlestrippath KindleStripPath��  ��  � m    �� ���   � l   "������ n    "��� 1     "��
�� 
strq� o     ���� 0 origfilepath origFilePath��  ��  � m   # $�� ���   � l  % (������ n   % (��� 1   & (��
�� 
strq� o   % &���� $0 strippedfilepath strippedFilePath��  ��  � o      ���� 0 shellcommand  � ��� Q   , A���� r   / 6��� I  / 4�����
�� .sysoexecTEXT���     TEXT� o   / 0���� 0 shellcommand  ��  � o      ���� 0 shellresult  � R      ����
�� .ascrerr ****      � ****� l     ������ o      ���� 0 error_message  ��  ��  � �����
�� 
errn� l     ������ o      ���� 0 error_number  ��  ��  ��  � r   > A��� o   > ?���� 0 error_message  � o      ���� 0 shellresult  � ��� Z   B �������� G   B i��� ?   B Q��� l  B O������ I  B O�����
�� .sysooffslong    ��� null��  � ����
�� 
psof� m   D E�� ��� 
 E r r o r� �����
�� 
psin� o   H I���� 0 shellresult  ��  ��  ��  � m   O P����  � ?   T e��� l  T c������ I  T c�����
�� .sysooffslong    ��� null��  � ����
�� 
psof� m   V Y�� ���  W a r n i n g� �����
�� 
psin� o   \ ]���� 0 shellresult  ��  ��  ��  � m   c d����  � k   l ��� ��� r   l |��� I  l z�� 
�� .rdwropenshor       file  4   l r��
�� 
file o   p q���� 0 resultsfile resultsFile ����
�� 
perm m   u v��
�� boovtrue��  � o      ���� 0 fileref fileRef�  I  } ���
�� .rdwrseofnull���     **** o   } ~���� 0 fileref fileRef ����
�� 
set2 m   � �����  ��   	
	 I  � ���
�� .rdwrwritnull���     **** o   � ����� 0 shellresult   ����
�� 
refn o   � ����� 0 fileref fileRef��  
 �� I  � �����
�� .rdwrclosnull���     **** o   � ����� 0 fileref fileRef��  ��  ��  ��  � �� L   � �����  ��  �  l     ��������  ��  ��    i     I     ������
�� .aevtoappnull  �   � ****��  ��   Z     ���� l    ���� I     �������� (0 getexecutablepaths GetExecutablePaths��  ��  ��  ��   k      r     m    	 �   � D r a g   &   D r o p   i m a g e s   f o l d e r s   o n t o   t h i s   A p p l e s c r i p t   a p p l i c a t i o n   t o   c o n v e r t   t h e m   t o   a   P a n e l V i e w   M o b i p o c k e t   e b o o k s . o      ���� 0 
dialogtext 
dialogText !��! I   ��"#
�� .sysodlogaskr        TEXT" o    ���� 0 
dialogtext 
dialogText# ��$%
�� 
appr$ m    && �'' ( K i n d l e C o m i c C o n v e r t e r% ��()
�� 
btns( J    ** +��+ m    ,, �--  O K��  ) ��.��
�� 
dflt. m    ���� ��  ��  ��  ��   /0/ l     �������  ��  �  0 121 i     #343 I     �~5�}
�~ .aevtodocnull  �    alis5 o      �|�| 0 
some_items  �}  4 Z     �67�{�z6 l    8�y�x8 I     �w�v�u�w (0 getexecutablepaths GetExecutablePaths�v  �u  �y  �x  7 X    �9�t:9 k    �;; <=< O   $>?> l 	  #@�s�r@ r    #ABA c    !CDC l   E�q�pE n    FGF m    �o
�o 
ctnrG o    �n�n 0 	this_item  �q  �p  D m     �m
�m 
ctxtB o      �l�l 0 parentfolder ParentFolder�s  �r  ? m    HH�                                                                                  MACS  alis    t  Macintosh HD               �8�H+     N
Finder.app                                                      �S��        ����  	                CoreServices    �8҈      �͒       N   H   G  6Macintosh HD:System: Library: CoreServices: Finder.app   
 F i n d e r . a p p    M a c i n t o s h   H D  &System/Library/CoreServices/Finder.app  / ��  = IJI Z   % hKL�kMK l  % .N�j�iN =  % .OPO n   % ,QRQ 1   * ,�h
�h 
asdrR l  % *S�g�fS I  % *�eT�d
�e .sysonfo4asfe        fileT o   % &�c�c 0 	this_item  �d  �g  �f  P m   , -�b
�b boovfals�j  �i  L k   1 ZUU VWV r   1 6XYX c   1 4Z[Z o   1 2�a�a 0 	this_item  [ m   2 3�`
�` 
ctxtY o      �_�_ 0 filename fileNameW \�^\ Z   7 Z]^�]_] E   7 :`a` o   7 8�\�\ 0 filename fileNamea m   8 9bb �cc  .^ k   = Tdd efe r   = Bghg m   = >ii �jj  .h n     klk 1   ? A�[
�[ 
txdll 1   > ?�Z
�Z 
ascrf m�Ym r   C Tnon c   C Rpqp l  C Nr�X�Wr n   C Nsts 7 D N�Vuv
�V 
citmu m   H J�U�U v m   K M�T�T��t o   C D�S�S 0 filename fileName�X  �W  q m   N Q�R
�R 
TEXTo o      �Q�Q 0 dir  �Y  �]  _ r   W Zwxw o   W X�P�P 0 filename fileNamex o      �O�O 0 dir  �^  �k  M k   ] hyy z{z r   ] b|}| c   ] `~~ o   ] ^�N�N 0 	this_item   m   ^ _�M
�M 
ctxt} o      �L�L 0 filename fileName{ ��K� r   c h��� c   c f��� o   c d�J�J 0 	this_item  � m   d e�I
�I 
ctxt� o      �H�H 0 dir  �K  J ��� r   i |��� I  i z�G��F
�G .sysoexecTEXT���     TEXT� b   i v��� m   i l�� ���  b a s e n a m e  � l  l u��E�D� n   l u��� 1   q u�C
�C 
strq� l  l q��B�A� n   l q��� 1   m q�@
�@ 
psxp� o   l m�?�? 0 dir  �B  �A  �E  �D  �F  � o      �>�> 0 dirname  � ��� r   } ���� I  } ��=��
�= .sysodlogaskr        TEXT� b   } ���� m   } ��� ��� 2 E n t e r   a   t i t l e   f o r   f o l d e r  � l  � ���<�;� n   � ���� 1   � ��:
�: 
strq� o   � ��9�9 0 dirname  �<  �;  � �8��7
�8 
dtxt� o   � ��6�6 0 dirname  �7  � o      �5�5 0 temp  � ��� r   � ���� l  � ���4�3� n   � ���� 1   � ��2
�2 
ttxt� o   � ��1�1 0 temp  �4  �3  � o      �0�0 0 thetitle TheTitle� ��� I   � ��/��.�/ 0 comic2ebook Comic2Ebook� ��-� o   � ��,�, 0 filename fileName�-  �.  � ��� I   � ��+��*�+ 0 	kindlegen 	Kindlegen� ��)� o   � ��(�( 0 dir  �)  �*  � ��'� I   � ��&��%�& 0 	stripfile 	StripFile� ��$� o   � ��#�# 0 dir  �$  �%  �'  �t 0 	this_item  : o    �"�" 0 
some_items  �{  �z  2 ��!� l     � ���   �  �  �!       ���������������������  � ���������������
�	��� (0 getcomic2ebookpath GetComic2EbookPath� $0 getkindlegenpath GetKindlegenPath� (0 getkindlestrippath GetKindleStripPath� (0 getexecutablepaths GetExecutablePaths� 0 comic2ebook Comic2Ebook� 0 	kindlegen 	Kindlegen� 0 	stripfile 	StripFile
� .aevtoappnull  �   � ****
� .aevtodocnull  �    alis� "0 comic2ebookpath comic2ebookPath� 0 kindlegenpath kindlegenPath� "0 kindlestrippath KindleStripPath� 0 parentfolder ParentFolder� 0 thetitle TheTitle�
  �	  �  �  � �  ������ (0 getcomic2ebookpath GetComic2EbookPath�  �  � �� 0 
fileexists  � �� ���� 0���� A���� J�� N�� T������
� 
file
�  
rtyp
�� 
ctxt
�� .earsffdralis        afdr
�� 
psxp�� "0 comic2ebookpath comic2ebookPath
�� 
psxf
�� .coredoexbool        obj 
�� 
appr
�� 
btns
�� 
dflt�� 
�� .sysodlogaskr        TEXT� H*�)��l �%/�,E�OfE�O� ��&j 	 eE�Y hUO� �����kv�ka  Y hO�� �� ^���������� $0 getkindlegenpath GetKindlegenPath��  ��  � ���� 0 
fileexists  � �� h���� y���� ��� ��� �������
�� 
file
�� 
psxp�� 0 kindlegenpath kindlegenPath
�� 
psxf
�� .coredoexbool        obj 
�� 
appr
�� 
btns
�� 
dflt�� 
�� .sysodlogaskr        TEXT�� >*��/�,E�OfE�O� ��&j  eE�Y hUO� �����kv�k� Y hO�� �� ����������� (0 getkindlestrippath GetKindleStripPath��  ��  � ���� 0 
fileexists  � �������� ����� ����� ��� ��� �������
�� 
file
�� 
rtyp
�� 
ctxt
�� .earsffdralis        afdr
�� 
psxp�� "0 kindlestrippath KindleStripPath
�� 
psxf
�� .coredoexbool        obj 
�� 
appr
�� 
btns
�� 
dflt�� 
�� .sysodlogaskr        TEXT�� H*�)��l �%/�,E�OfE�O� ��&j 	 eE�Y hUO� �����kv�ka  Y hO�� �� ����������� (0 getexecutablepaths GetExecutablePaths��  ��  �  � ���������� (0 getcomic2ebookpath GetComic2EbookPath�� $0 getkindlegenpath GetKindlegenPath
�� 
bool�� (0 getkindlestrippath GetKindleStripPath�� *j+  	 	*j+ �&	 	*j+ �&� �� ����������� 0 comic2ebook Comic2Ebook�� ����� �  ���� 0 dir  ��  � ���������������� 0 dir  �� 0 dirpath dirPath�� 0 resultsfile resultsFile�� 0 shellcommand  �� 0 shellresult  �� 0 error_message  �� 0 error_number  � ���� � �����	���������)������2����8��
�� 
psxp�� 0 parentfolder ParentFolder�� "0 comic2ebookpath comic2ebookPath
�� 
strq�� 0 thetitle TheTitle
�� .sysoexecTEXT���     TEXT�� 0 error_message  � ������
�� 
errn�� 0 error_number  ��  
�� 
psof
�� 
psin�� 
�� .sysooffslong    ��� null
�� 
bool
�� 
appr
�� .sysodlogaskr        TEXT�� k��,E�O��%E�O���,%�%��,%�%��,%E�O �j 	E�W 
X 
 �E�O*���� j
 *�a �� ja & �a a l Y hOh� ��@���������� 0 	kindlegen 	Kindlegen�� ����� �  ���� 0 dir  ��  � ���������������� 0 dir  �� 0 opfpath opfPath�� 0 resultsfile resultsFile�� 0 shellcommand  �� 0 shellresult  �� 0 error_message  �� 0 error_number  � ��L��T��^���������~��������������
�� 
psxp�� 0 parentfolder ParentFolder�� 0 kindlegenpath kindlegenPath
�� 
strq
�� .sysoexecTEXT���     TEXT�� 0 error_message  � ������
�� 
errn�� 0 error_number  ��  
�� 
psof
�� 
psin�� 
�� .sysooffslong    ��� null
�� 
bool
�� 
appr
�� .sysodlogaskr        TEXT�� a��,�%E�O��%E�O��%��,%E�O �j E�W 
X  	�E�O*���� j
 *���� ja & �a a l Y hOh� ������������� 0 	stripfile 	StripFile�� ����� �  ���� 0 dir  ��  � 	�������������������� 0 dir  �� 0 origfilepath origFilePath�� $0 strippedfilepath strippedFilePath�� 0 resultsfile resultsFile�� 0 shellcommand  �� 0 shellresult  �� 0 error_message  �� 0 error_number  �� 0 fileref fileRef� ����������~�}���|�{��z��y�x�w��v�u�t�s�r�q�p�o�n
�� 
psxp�� 0 parentfolder ParentFolder� 0 thetitle TheTitle�~ "0 kindlestrippath KindleStripPath
�} 
strq
�| .sysoexecTEXT���     TEXT�{ 0 error_message  � �m�l�k
�m 
errn�l 0 error_number  �k  
�z 
psof
�y 
psin�x 
�w .sysooffslong    ��� null
�v 
bool
�u 
file
�t 
perm
�s .rdwropenshor       file
�r 
set2
�q .rdwrseofnull���     ****
�p 
refn
�o .rdwrwritnull���     ****
�n .rdwrclosnull���     ****�� ���,�%E�O��,�%�%E�O��%E�O���,%�%��,%�%��,%E�O �j E�W 
X  �E�O*��a �a  j
 *�a a �a  ja & /*a �/a el E�O�a jl O�a �l O�j Y hOh� �j�i�h���g
�j .aevtoappnull  �   � ****�i  �h  �  � 
�f�e�d&�c,�b�a�`�f (0 getexecutablepaths GetExecutablePaths�e 0 
dialogtext 
dialogText
�d 
appr
�c 
btns
�b 
dflt�a 
�` .sysodlogaskr        TEXT�g *j+   �E�O�����kv�k� 	Y h� �_4�^�]���\
�_ .aevtodocnull  �    alis�^ 0 
some_items  �]  � �[�Z�Y�X�W�V�[ 0 
some_items  �Z 0 	this_item  �Y 0 filename fileName�X 0 dir  �W 0 dirname  �V 0 temp  � �U�T�S�RH�Q�P�O�N�Mbi�L�K�J�I�H��G�F�E��D�C�B�A�@�?�>�U (0 getexecutablepaths GetExecutablePaths
�T 
kocl
�S 
cobj
�R .corecnte****       ****
�Q 
ctnr
�P 
ctxt�O 0 parentfolder ParentFolder
�N .sysonfo4asfe        file
�M 
asdr
�L 
ascr
�K 
txdl
�J 
citm�I��
�H 
TEXT
�G 
psxp
�F 
strq
�E .sysoexecTEXT���     TEXT
�D 
dtxt
�C .sysodlogaskr        TEXT
�B 
ttxt�A 0 thetitle TheTitle�@ 0 comic2ebook Comic2Ebook�? 0 	kindlegen 	Kindlegen�> 0 	stripfile 	StripFile�\ �*j+   � ��[��l kh � 	��,�&E�UO�j �,f  .��&E�O�� ���,FO�[�\[Zk\Z�2a &E�Y �E�Y ��&E�O��&E�Oa �a ,a ,%j E�Oa �a ,%a �l E�O�a ,E` O*�k+ O*�k+ O*�k+ [OY�cY h� ��� � / U s e r s / l e s t a t / A p p l i c a t i o n s / k c c / K i n d l e C o m i c C o n v e r t e r . a p p / C o n t e n t s / R e s o u r c e s / c o m i c 2 e b o o k . p y� ��� 0 / u s r / l o c a l / b i n / k i n d l e g e n� ��� � / U s e r s / l e s t a t / A p p l i c a t i o n s / k c c / K i n d l e C o m i c C o n v e r t e r . a p p / C o n t e n t s / R e s o u r c e s / k i n d l e s t r i p . p y� ��� ` M a c i n t o s h   H D : U s e r s : l e s t a t : A p p l i c a t i o n s : k c c : t e s t :� ���  t e s t�  �  �  �   ascr  ��ޭ