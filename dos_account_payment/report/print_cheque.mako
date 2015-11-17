<html>
<head>
	<style>
			.vtop
			{
				vertical-align: top;
			}

			.vbottom
			{
				vertical-align: bottom;
			}
		
			.hright
			{
				text-align: right;
				padding-right: 3px;
			}
			.hleft
			{
				text-align: left;
			}
			.hmid
			{
				text-align: center;
			}
			.content
			{
				font-size: 12px;
			}
			.border_grey
			{
				border: 1px solid lightGrey;
			}
			.border_black
			{
				border: 1px solid black;
			}
			.space
			{
				min-height: 25px;
			}
			.note
			{
				width: 500px;
				padding: 5px;
				float:right;
				min-width: 100px;
				border:1px solid black;
			}
			.padding
			{
				padding: 5px;
			}
			.paddingtop
			{
				padding-top: 10px;
			}
			.paddingright
			{
				padding-right: 10px;
			}
			th
			{
				font-size: 12px;
				border-bottom: 1px solid black;
			}
			#border_bottom_grey
			{
				border-bottom: 1px solid lightGrey;
			}
			.background_color
			{
				background-color: lightGrey
			}
			.border_top
			{
				border-top: 1px solid black;
			}
			.border_bottom
			{
				border-bottom: 1px solid black;
			}
			.border_right
			{
				border-right: 1px solid black;
			}
			.border_top_bottom
			{
				border-top: 1px solid black;
				border-bottom: 1px solid black;
			}
			.border_left_right
			{
				border-right: 1px solid black;
				border-left: 1px solid black;
			}
			.fright
			{
				float: right; 
			}
			.fleft
			{
				float: left; 
			}
			.font12px
			{
				font-size: 12px;
			}
			.font10px
			{
				font-size: 10px;
			}
			.font14px
			{
				font-size: 14px;
			}
			.font16px
			{
				font-size: 16px;
			}
			.font22px
			{
				font-size: 22px;
			}
			.font30px
			{
				font-size: 30px;
			}
			.title 
			{
				font-size: 22px;
				text-align: center;
				padding: 5px;
			}
			.title-table 
			{
				font-size: 12px;
				text-align:center;
				padding-top:20px;
			}
			
         	table.one 
         	{border-collapse:collapse;}
			
			#watermark {
			  color: #d0d0d0;
			  text-align:center;
			  font-size: 80pt;
			  -webkit-transform: rotate(-45deg);
			  position: fixed;
			  width: 500px;
			  height: 500px;
			  margin: 0;
			  z-index: -1;
			  left:130px;
			  top:150px;
				}
		</style>
</head>
<body>
	%for o in objects :
	
	<table class="header" style="border-bottom: 0px solid black; width: 100%">
            <tr>
            	<td colspan="3" class="font10px" align="right">Form No. : EPN/FIN/F-001
            	</td>
            </tr>
            <tr>
                <td style="width: 20%" height="10px">${helper.embed_company_logo()|safe}</td>
	            <td>
	            	<table>
	            		<tr>
	            			<td style="width: 80%" class="font16px"><b>PT ENERGIA PRIMA NUSANTARA<b></td>
	            		</tr>
	            		<tr>
	            			<td style="width: 80%">Head Office - JIEP</td>
	            		</tr>
	            	
	            	</table>
	            </td>
	            <td>
	            	<table>
	            		<tr rowspan="2">
	            			<td class="font30px" align="center"><b>PV</b>
	            			</td>
	            		</tr>
	            	</table>
	            </td>
            </tr>
            <tr>
            	<td><br/>
            	</td>
            <tr>
	</table>
	<table cellpadding="2px" width="100%" class="font12px one">
		<tr >
			<td colspan="3" class="font16px"><b>PAYMENT VOUCHER (${o.number})</b>
			</td>
		</tr>
		<tr>
			<td  width="20%">PAID TO</td>
			<td>: ${o.partner_id.name}</td>
			<td  width="10%">No</td>
			<td>: </td>
		</tr>
		<tr>
			<td width="20%">AMOUNT</td>
			<td>: ${o.company_id.currency_id.symbol} ${formatLang(o.amount) or formatLang(0)}</td>
			<td>DATE</td>
			<td>: ${time.strftime('%d-%m-%Y', time.strptime( o.date,'%Y-%m-%d'))}</td>
		</tr>
		<tr>
			<td></td>
			<td></td>
			<td></td>
			<td><br/></td>
		</tr>
		<tr>
			<td width="20%">BANK</td>
			<td>: ${o.partner_id.bank_ids[0].name or ''}</td>
			<td></td>
			<td></td>
		</tr>
		<tr>
			<td></td>
			<td></td>
			<td></td>
			<td><br/></td>
		</tr>
	</table>
	<table  cellpadding="5px" width="100%" class="font12px one">
		<tr bgcolor="#d3d3d3">
			<td width="20%" padding-top="10px" class="border_top_bottom border_left_right hmid">ACCOUNT CODE</td>
			<td width="50%" padding-top="10px" class="border_top_bottom border_left_right hmid">PARTICULAR</td>
			<td width="30%" padding-top="10px" class="border_top_bottom border_left_right hmid">AMOUNT</td>
		</tr>
		%for x in o.line_dr_ids :
			%if x.amount > 0
		<tr>
			
			<td width="20%" class=" border_left_right hmid">${x.move_line_id.move_id.line_id[1].account_id.code}</td>
			<td width="50%" class=" border_left_right hleft">${x.move_line_id.move_id.line_id[1].name}</td>
			<td width="30%" class=" border_left_right hright">${o.company_id.currency_id.symbol} ${formatLang(x.amount) or ''}</td>
		</tr>
			%endif
		
		<tr>
			<td width="20%" class=" border_left_right hmid"></td>
			<td width="50%" class=" border_left_right hright"></td>
			<td width="30%" class=" border_left_right hright"><br/><br/></td>
		</tr>
		<tr>
			<td width="20%" class="border_bottom border_left_right hmid"></td>
			<td width="50%" class="border_bottom border_left_right hright">TOTAL</td>
			<td width="30%" class="border_bottom border_left_right hright">${o.company_id.currency_id.symbol} ${formatLang(x|sum(attribute='amount')) or ''}</td>
		</tr>
		%endfor
		<tr>
			<td ></td>
			<td ></td>
			<td >
				<br/>
				
			</td>
		</tr>
		<tr>
			<td width="20%" >PAYMENT USING</td>
			<td >: xxxx</td>
			<td >
				
			</td>
		</tr>
		<tr>
			<td width="20%" >BANK</td>
			<td >: xxxx</td>
			<td >
				
			</td>
		</tr>
		<tr>
			<td >DATE</td>
			<td >: ${time.strftime('%d-%m-%Y', time.strptime( o.date,'%Y-%m-%d'))}</td>
			<td >
				
			</td>
		</tr>
		<tr>
			<td >AMOUNT</td>
			<td >: ${o.company_id.currency_id.symbol} ${formatLang(o.amount) or formatLang(0)}</td>
			<td >
				
			</td>
		</tr>
		<tr>
			<td ></td>
			<td ></td>
			<td >
				<br/>
				<br/>
				<br/>
			</td>
		</tr>
	
	</table>
	<table cellpadding="2px"  width="100%" class="font12px one">
		<tr>
			<td width="20" class="hmid">RECEIVED BY :</td>
			<td width="20"></td>
			<td width="20" class="hmid">CHECKED BY :</td>
			<td width="20"></td>
			<td width="20" class="hmid">REQUEST BY :</td>
		</tr>
		<tr>
			<td>
				<br/>
				<br/>
				<br/>
				<br/>
				
			</td>
		</tr>
		<tr>
			<td class="border_bottom"></td>
			<td></td>
			<td class="border_bottom"></td>
			<td></td>
			<td class="border_bottom"></td>
		</tr>
	</table>
	
	
	
	%endfor
	
	
	
</body>
</html>