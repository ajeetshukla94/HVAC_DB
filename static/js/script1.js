var frame_count = 1;  

$(document).ready(function(){
    $('body').append($('<script src="static/js/md5.min.js"></script>'));
});

function add_row(elem){
	
	var row_index = elem.parentElement.parentElement.children[0].rows.length - 1;
	var row = elem.parentElement.parentElement.children[0].rows[row_index];
    var table = elem.parentElement.parentElement.children[0];
    var clone = row.cloneNode(true);
	var cells_length = clone.cells.length - 1;
	for(var i = 1; i<cells_length; i++){
		clone.cells[i].children[0].value=""
	}
    table.appendChild(clone);
}

function delete_row(elem){
	if(elem.parentElement.parentElement.parentElement.rows.length > 2){
		elem.parentElement.parentElement.remove();
	}else{
		alert("First row can not be deleted!")
	}
}


function submit(){
	
	
	var frame_list = document.getElementsByClassName("frame");
	var basic_details = {};
	if ($('#company_name').val()=="")
	{
		alert("Please select company Name");
		return;
	}
	if ($('#grade').val()=="")
	{
		alert("Please select Grade");
		return ;
	}


	if ($('#ahu_number').val()=="" && $('#grade').val()!="A")
	{
		alert("Please Enter Equipment ID");
		return ;
	}
	if ($('#room_name').val()=="" && $('#grade').val()!="A" )
	{
		alert("Please Room Equipment Name");
		return ;
	}
	
	if ($('#ahu_number').val()=="" && $('#grade').val()=="A")
	{
		alert("Please Enter AHU Number");
		return ;
	}
	if ($('#room_name').val()=="" && $('#grade').val()=="A" )
	{
		alert("Please Room Name");
		return ;
	}





	if ($('#room_volume').val()=="" && $('#grade').val()!="A")
	{
		alert("Please enter Room Volume");
		return ;
	}	
		
	if ($('#acph_thresold').val()=="" && $('#grade').val()!="A")
	{
		alert("Please enter ACPH Thresold");
		return ;
	}	
	if ($('#SR_NO').val()=="")
	{
		alert("Please select Serail Number");
		return ;
	}
	if ($('#location').val()=="")
	{
		alert("Please enter Department ");
		return ;
	}
	if ($('#Test_taken').val()=="")
	{
		alert("Please Enter Test_taken Date");
		return ;
	}
	var MAKE_MODEL = $('#MAKE_MODEL').val()
	var full_data = {};
	var final_table_data= {};
	basic_details['sr_no'] =$('#SR_NO').val();
	basic_details['company_name'] =$('#company_name').val();
	basic_details['room_volume'] =$('#room_volume').val();
	basic_details['room_name'] =$('#room_name').val();
	basic_details['ahu_number'] =$('#ahu_number').val();	
	basic_details['location'] =$('#location').val();
	basic_details['Test_taken'] =$('#Test_taken').val();
	basic_details['grade'] =$('#grade').val();
	basic_details['acph_thresold'] =$('#acph_thresold').val();
		
	code_tbl = frame_list[0].getElementsByClassName("code_tbl")[0]
	code_rows = code_tbl.rows
	for(var j = 1; j<code_rows.length; j++)
	{
		tds = code_rows[j].children
		
		if (tds[0].firstElementChild.value=="")
		{	
				alert("Filter ID number cannot be blank in row : "+j);
				return;
		}
		
		for(var l = 1; l<6; l++)
		{

			if (tds[l].firstElementChild.value=="")
			{	
				alert("Please enter correct value for V"+l+" in row : "+j);
				return;
			}
			if (MAKE_MODEL !="HSTENI")
			{
				if (tds[l].firstElementChild.value % 10!=0)
				{
					alert("Please enter number divisble by 10 for V"+l+" in row : "+j);
					return;
				}
			}
		}
		
		if (tds[6].firstElementChild.value=="" && $('#grade').val()!="A" )
		{	
				alert("Inlet Size cannot be blank in row : "+j);
				return;
		}
		
		
		
		
		
	}
	for(var j = 1; j<code_rows.length; j++){
		
		tds = code_rows[j].children
		Label_number = tds[0].firstElementChild.value
		V1 = tds[1].firstElementChild.value
		V2 = tds[2].firstElementChild.value
		V3 = tds[3].firstElementChild.value
		V4 = tds[4].firstElementChild.value
		V5 = tds[5].firstElementChild.value
		
		
		var table_data = {};
		table_data['Label_number'] =Label_number 
		table_data['V1'] =V1
		table_data['V2'] =V2
		table_data['V3'] =V3
		table_data['V4'] =V4
		table_data['V5'] =V5
        if ($('#grade').val()=="A" )
		{
			inlet_size = ""
		}
		else
	    { 
			inlet_size = tds[6].firstElementChild.value
		}
		table_data['Inlet_size'] =inlet_size
		final_table_data[j] = table_data
	}
	
	full_data['observation']=final_table_data
	full_data['basic_details']=basic_details
	
	
	$.getJSON('/submit_air_velocity', 
	{
		params_data : JSON.stringify(full_data)
	}, function(result) 
	{
		var link = document.createElement('a')
		link.href =result.file_path;
		link.download = result.file_name;
		link.dispatchEvent(new MouseEvent('click'));
		

		
	});
	
}


function submit_consolidated(){
	
	if ($('#company_name').val()=="")
	{
		alert("Please select company Name");
		return;
	}
	
	if ($('#report_type').val()=="")
	{
		alert("Please Select Report Type");
		return ;
	}
	if ($('#start_date').val()=="")
	{
		alert("Please enter Start Date");
		return ;
	}
	if ($('#end_date').val()=="")
	{
		alert("Please enter end Date");
		return ;
	}
	var full_data = {};
	full_data['company_name'] = $('#company_name').val()
	full_data['report_type']  = $('#report_type').val()
	full_data['start_date']   = $('#start_date').val()
	full_data['end_date']     = $('#end_date').val()
	
	
	$.getJSON('/submit_consolidated', 
	{
		params_data : JSON.stringify(full_data)
	}, function(result) 
	{
		alert(result.msg);
		
	});
	
}



function submit_pao(){
	
	
	var frame_list = document.getElementsByClassName("frame");
	var basic_details = {};
	if ($('#company_name').val()=="")
	{
		alert("Please select company Name");
		return;
	}
	
	if ($('#ahu_number').val()=="")
	{
		alert("Please Enter AHU Number");
		return ;
	}
	if ($('#room_name').val()=="")
	{
		alert("Please Room Name");
		return ;
	}
	if ($('#SR_NO').val()=="")
	{
		alert("Please select Serail Number");
		return ;
	}
	if ($('#location').val()=="")
	{
		alert("Please enter Department ");
		return ;
	}
	if ($('#Test_taken').val()=="")
	{
		alert("Please Enter Test_taken Date");
		return ;
	}
	
	if ($('#compresed_value').val()=="")
	{
		alert("Please Enter Compressed Air Value");
		return ;
	}
	
	var MAKE_MODEL = $('#MAKE_MODEL').val()
	var full_data = {};
	var final_table_data= {};
	basic_details['sr_no'] =$('#SR_NO').val();
	basic_details['company_name'] =$('#company_name').val();
	basic_details['room_name'] =$('#room_name').val();
	basic_details['ahu_number'] =$('#ahu_number').val();	
	basic_details['location'] =$('#location').val();
	basic_details['Test_taken'] =$('#Test_taken').val();
	
	basic_details['compresed_value'] =$('#compresed_value').val();
	basic_details['check_val'] =$('#check_val').val();
	
		
	code_tbl = frame_list[0].getElementsByClassName("code_tbl")[0]
	code_rows = code_tbl.rows
	for(var j = 1; j<code_rows.length; j++)
	{
		tds = code_rows[j].children
		
		if (tds[0].firstElementChild.value=="")
		{	
				alert("Filter ID number cannot be blank in row : "+j);
				return;
		}
		
		if (tds[0].firstElementChild.value=="")
		{	
				alert("Filter INLET NUMBER cannot be blank in row : "+j);
				return;
		}
		
		
		if (tds[1].firstElementChild.value=="")
		{	
				alert("Filter Upstream cannot be blank in row : "+j);
				return;
		}
		
		
		
		if (tds[2].firstElementChild.value=="")
		{	
				alert("Filter Leakage cannot be blank in row : "+j);
				return;
		}
		
		if (tds[3].firstElementChild.value=="")
		{	
				alert("Filter Remark cannot be blank in row : "+j);
				return;
		}
		
		
		
		
		
	}
	for(var j = 1; j<code_rows.length; j++){
		
		tds = code_rows[j].children
		INLET_NUMBER = tds[0].firstElementChild.value
		Upstream = tds[1].firstElementChild.value
		Leakage = tds[2].firstElementChild.value
		Remark = tds[3].firstElementChild.value
		
		var table_data = {};
		table_data['INLET_NUMBER'] =INLET_NUMBER 
		table_data['Upstream'] =Upstream
		table_data['Leakage'] =Leakage
		table_data['Remark'] =Remark
		final_table_data[j] = table_data
	}
	
	full_data['observation']=final_table_data
	full_data['basic_details']=basic_details
	
	
	$.getJSON('/submit_data_pao', 
	{
		params_data : JSON.stringify(full_data)
	}, function(result) 
	{
		var link = document.createElement('a')
		link.href =result.file_path;
		link.download = result.file_name;
		link.dispatchEvent(new MouseEvent('click'));
		

		
	});
	
}




function submit_particle_report(){
	
	
	var frame_list = document.getElementsByClassName("frame");
	var basic_details = {};
	if ($('#company_name').val()=="")
	{
		alert("Please select company Name");
		return;
	}
	
	if ($('#ahu_number').val()=="")
	{
		alert("Please Enter AHU Number");
		return ;
	}
	if ($('#room_name').val()=="")
	{
		alert("Please Room Name");
		return ;
	}	
	if ($('#SR_NO').val()=="")
	{
		alert("Please select Serail Number");
		return ;
	}
	if ($('#location').val()=="")
	{
		alert("Please enter Department ");
		return ;
	}
	if ($('#grade').val()=="")
	{
		alert("Please Select Grade ");
		return ;
	}
	if ($('#condition').val()=="")
	{
		alert("Please Select condition");
		return ;
	}
	if ($('#Test_taken').val()=="")
	{
		alert("Please Enter Test_taken Date");
		return ;
	}
	
	if ($('#gl_value').val()=="")
	{
		alert("Please Select Guidelines");
		return ;
	}
	
	
	var MAKE_MODEL = $('#MAKE_MODEL').val()
	var full_data = {};
	var final_table_data= {};
	basic_details['sr_no'] =$('#SR_NO').val();
	basic_details['company_name'] =$('#company_name').val();
	basic_details['room_name'] =$('#room_name').val();
	basic_details['ahu_number'] =$('#ahu_number').val();	
	basic_details['location'] =$('#location').val();
	basic_details['Test_taken'] =$('#Test_taken').val();
	basic_details['condition'] =$('#condition').val();
	basic_details['grade'] =$('#grade').val();
	basic_details['gl_value'] =$('#gl_value').val();
	
	
		
	code_tbl = frame_list[0].getElementsByClassName("code_tbl")[0]
	code_rows = code_tbl.rows
	for(var j = 1; j<code_rows.length; j++)
	{
		tds = code_rows[j].children
		
		if (tds[0].firstElementChild.value=="")
		{	
				alert("Filter Location cannot be blank in row : "+j);
				return;
		}
		
		if (tds[1].firstElementChild.value=="")
		{	
				alert("Filter ≥ 0.5 μm cannot be blank in row : "+j);
				return;
		}
		
		
		if (tds[2].firstElementChild.value=="")
		{	
				alert("Filter ≥ 5.0 μm cannot be blank in row : "+j);
				return;
		}
		if (tds[3].firstElementChild.value=="")
		{	
				alert("Remark cannot be blank in row : "+j);
				return;
		}
		
		
		
		
	}
	for(var j = 1; j<code_rows.length; j++){
		
		tds = code_rows[j].children
		Location = tds[0].firstElementChild.value
		zeor_point_five = tds[1].firstElementChild.value
		five_point_zero = tds[2].firstElementChild.value
		remark = tds[3].firstElementChild.value
		
		
		var table_data = {};
		table_data['Location'] =Location 
		table_data['zeor_point_five'] =zeor_point_five
		table_data['five_point_zero'] =five_point_zero
		table_data['remark'] =remark
		final_table_data[j] = table_data
	}
	
	full_data['observation']=final_table_data
	full_data['basic_details']=basic_details
	
	
	$.getJSON('/submit_particle_report', 
	{
		params_data : JSON.stringify(full_data)
	}, function(result) 
	{
		var link = document.createElement('a')
		link.href =result.file_path;
		link.download = result.file_name;
		link.dispatchEvent(new MouseEvent('click'));
		

		
	});
	
}


$(function() 
{
    $("#company_name").change(function() 
    {
	company_name = $('option:selected',this).text();
	$.getJSON('/update_company_details', 
	{
		params_data : JSON.stringify(company_name)
	}, function(data) 
	{
		$('#company_address').val(data.company_address);
      	$('#report_id').val(data.report_id);
        $('#Test_taken').val(data.test_taken);		
		$('#location').val(data.location);							
	});
 });
});

$(function() 
{
	$("#SR_NO").change(function()
	{        
	SR_NO = $('option:selected',this).text();
	$.getJSON('/update_instument_details', 
	{
		params_data : JSON.stringify(SR_NO)
	}, function(data) 
	{			
		$('#INSTRUMENT_NAME').val(data.INSTRUMENT_NAME);
      	$('#MAKE_MODEL').val(data.MAKE);
        $('#VALIDITY').val(data.VALIDITY);							
	
	});
  });
});


$('#paotable').on('change', 'input', function () {
    var row = $(this).closest('tr');
   	var check_val = $('#check_val').val();
    var upstream  = $('#Upstream', row).val();
	var Leakage   = $('#Leakage', row).val();	
	
	if ((upstream!="") && (upstream<=80 &&  upstream>=20) && (Leakage!="" )&& (Leakage<=check_val))
	{
		$('#Remark', row).val("Pass");
	}	
	else {$('#Remark', row).val("Fail");}
	
	
	
});

var val_1;
var val_2;
$("#grade").change(function()
	{
        
	grade = $('option:selected',this).text();
	var full_data = {};
	full_data['grade'] = grade
	full_data['gl_value'] = $('#gl_value').val()
	full_data['condition'] = $('#condition').val()
   	
	if (grade=="A")
	{
		$("#acph_thresold").hide();
		$("#acph_thresold_label").hide();

        $("#room_volume_label").hide();
        $("#room_volume").hide();
        $("#Inlet_size_label").hide();
        $("#Inlet_size").hide();


		$("#ahu_number_label").text("Equipment ID");
		$("#room_name_label").text("Equipment Name");
	}
	else
	{
		$("#acph_thresold").show();
		$("#acph_thresold_label").show();	

        $("#room_volume_label").show();
        $("#room_volume").show();

		$("#Inlet_size_label").show();
        $("#Inlet_size").show();

		$("#ahu_number_label").text("AHU Number");
		$("#room_name_label").text("ROOM NAME");	
	}
	
	$.getJSON('/get_limits', 
	{
		params_data : JSON.stringify(full_data)
	}, function(data) 
	{		
			val_1 = data.value1 
			val_2 = data.value2
										
	});
    });
	
$('#particleCountTable').on('change', 'input', function () {
    var row = $(this).closest('tr');
    console.log(val_1)
	console.log(val_2)
	
	if (typeof(val_1)=="undefined" ||typeof(val_2)=="undefined")
	{
		alert("Please select Guildline and Grade");
		$('#five_point_zero', row).val("");
		$('#zeor_point_five', row).val("");
		$('#remark', row).val("");
		
		return ;
	}
	
    var zeor_point_five  = $('#zeor_point_five', row).val();
	var five_point_zero   = $('#five_point_zero', row).val();	
	
	if (zeor_point_five<=parseInt(val_1) && five_point_zero <= parseInt(val_2))
	{
			$('#remark', row).val("Pass");
	}	
	else {$('#remark', row).val("Fail");}
	
	
});


function updateCompanyDetails()
{
	code_tbl = document.getElementsByClassName("code_tbl")[0]
	code_rows = code_tbl.rows
	
	for(var j = 1; j<code_rows.length; j++)
	{
		tds = code_rows[j].children
		
		if (tds[0].firstElementChild.value=="")
		{	
				alert("Filter COMPANY NAME cannot be blank in row : "+j);
				return;
		}
		
		if (tds[1].firstElementChild.value=="")
		{	
				alert("Filter ADDRESS cannot be blank in row : "+j);
				return;
		}
		
		
		if (tds[2].firstElementChild.value=="")
		{	
				alert("Filter REPORT NUMBER  cannot be blank in row : "+j);
				return;
		}		
	}
	var final_table_data = {};
    var full_data = {};	
	for(var j = 1; j<code_rows.length; j++)
	{
		tds = code_rows[j].children	
		var table_data = {};
		table_data['COMPANY_NAME'] =tds[0].firstElementChild.value 	
		table_data['ADDRESS'] =tds[1].firstElementChild.value 	
		table_data['REPORT_NUMBER'] =tds[2].firstElementChild.value 		
		final_table_data[j] = table_data
	}
	
	full_data['observation']=final_table_data
	
	$.getJSON('/submit_updateCompanyDetails', 
	{
		params_data : JSON.stringify(full_data)
	}, function(result) 
	{
		alert("COMPANY DETAILS UPDATED");		
	});
	
}

function add_users()
{
	code_tbl = document.getElementsByClassName("code_tbl")[0]
	code_rows = code_tbl.rows
	
	for(var j = 1; j<code_rows.length; j++)
	{
		tds = code_rows[j].children
		
		if (tds[0].firstElementChild.value=="")
		{	
				alert("Filter Role cannot be blank in row : "+j);
				return;
		}
		
		if (tds[1].firstElementChild.value=="")
		{	
				alert("Filter First Name cannot be blank in row : "+j);
				return;
		}
		
		if (tds[2].firstElementChild.value=="")
		{	
				alert("Filter Last Name cannot be blank in row : "+j);
				return;
		}
		
		
		if (tds[3].firstElementChild.value=="")
		{	
				alert("Filter Password cannot be blank in row : "+j);
				return;
		}		
	}
	var final_table_data = {};
    var full_data = {};	
	for(var j = 1; j<code_rows.length; j++)
	{
		tds = code_rows[j].children	
		var table_data = {};
		table_data['Role'] =tds[0].firstElementChild.value 	
		table_data['fname'] =tds[1].firstElementChild.value 
		table_data['lname'] =tds[2].firstElementChild.value 
		salted_pass = tds[3].firstElementChild.value
		table_data['email'] = tds[4].firstElementChild.value
		encrypted_pass = md5(salted_pass)	
		table_data['Password'] = encrypted_pass		
		final_table_data[j] = table_data
	}
	
	full_data['observation']=final_table_data
	
	$.getJSON('/submit_add_user', 
	{
		params_data : JSON.stringify(full_data)
	}, function(result) 
	{
		alert("Users Added kindly note down usernam-"+result.userID);		
	});
	
}
function updateinstrumentDetails()
{
	code_tbl = document.getElementsByClassName("code_tbl")[0]
	code_rows = code_tbl.rows	
	for(var j = 1; j<code_rows.length; j++)
	{
		tds = code_rows[j].children		
		if (tds[0].firstElementChild.value=="")
		{	
				alert("Filter Type cannot be blank in row : "+j);
				return;
		}		
		if (tds[1].firstElementChild.value=="")
		{	
				alert("Filter EQUIPMENT NAME cannot be blank in row : "+j);
				return;
		}	
		if (tds[2].firstElementChild.value=="")
		{	
				alert("Filter MAKE cannot be blank in row : "+j);
				return;
		}			
		if (tds[3].firstElementChild.value=="")
		{	
				alert("Filter MODEL NUMBER cannot be blank in row : "+j);
				return;
		}			
		if (tds[4].firstElementChild.value=="")
		{	
				alert("Filter SR NO ID cannot be blank in row : "+j);
				return;
		}			
		if (tds[5].firstElementChild.value=="")
		{	
				alert("Filter DONE DATE cannot be blank in row : "+j);
				return;
		}			
		if (tds[6].firstElementChild.value=="")
		{	
				alert("Filter DUE DATE cannot be blank in row : "+j);
				return;
		}
		if (tds[7].firstElementChild.value=="")
		{	
				alert("Filter STATUS  cannot be blank in row : "+j);
				return;
		}			
	}	
	
	var final_table_data = {};
    var full_data = {};	
	for(var j = 1; j<code_rows.length; j++)
	{
		tds = code_rows[j].children	
		var table_data = {};
		table_data['Type']  = tds[0].firstElementChild.value 	
		table_data['EQUIPMENT_NAME']       = tds[1].firstElementChild.value 	
		table_data['MAKE'] = tds[2].firstElementChild.value 
		table_data['MODEL_NUMBER']  = tds[3].firstElementChild.value 	
		table_data['SR_NO_ID']       = tds[4].firstElementChild.value 	
		table_data['DONE_DATE'] = tds[5].firstElementChild.value 	
		table_data['DUE_DATE']  = tds[6].firstElementChild.value 		
		table_data['STATUS']    = tds[7].firstElementChild.value 	
		table_data['ISSUED_TO'] = tds[8].firstElementChild.value 
		table_data['COMPANY_NAME']    = tds[9].firstElementChild.value 	
		table_data['REMARK'] = tds[10].firstElementChild.value 
		final_table_data[j] = table_data
	}
	
	full_data['observation']=final_table_data
	
	$.getJSON('/submit_updateinstrumentDetails', 
	{
		params_data : JSON.stringify(full_data)
	}, function(result) 
	{
		alert("EQUIPMENT DETAILS UPDATED");	
        window.location.reload();		
	});
}

function request_instrument()
{
	selected_eq = $('input[name="selected_eq"]:checked').val();
	if (selected_eq==""  || selected_eq==undefined)
	{	
		alert("Please select Instrument");
		return;
	}	
	
	company_name = $('#company_name').val();
	if (company_name=="")
	{	
		alert("Please enter company name");
		return;
	}	
	
	REMARK = $('#remark').val();
	if (REMARK=="")
	{	
		alert("Please enter REMARK");
		return;
	}	
	
	var table_data = {};
	table_data['selected_eq']  = selected_eq
	table_data['company_name'] = company_name	
	table_data['REMARK'] = REMARK 
	
	$.getJSON('/push_instrument_request', 
	{
		params_data : JSON.stringify(table_data)
	}, function(result) 
	{
		alert("INSTRUMENT : "+selected_eq+" : HAS BEEN REQUESTED");	
		window.location.reload();
	});
	
}


function approve_deny_instrument()
{
	code_tbl = document.getElementsByClassName("code_tbl")[0]
	code_rows = code_tbl.rows	
	for(var j = 1; j<code_rows.length; j++)
	{
		tds = code_rows[j].children		
		if (tds[8].firstElementChild.value=="")
		{	
				alert("Filter APPROVE/DENY cannot be blank in row : "+j);
				return;
		}	

        if (tds[7].firstElementChild.value=="")
		{	
				alert("Filter REMARK cannot be blank in row : "+j);
				return;
		}			
	}	
	
	var final_table_data = {};
    var full_data = {};	
	for(var j = 1; j<code_rows.length; j++)
	{
		tds = code_rows[j].children	
		var table_data = {};
		table_data['APPROVE/DENY']  = tds[8].firstElementChild.value 		
		table_data['SR_NO_ID']       = tds[4].firstElementChild.value 
		table_data['REMARK']       = tds[7].firstElementChild.value	
		table_data['COMPANY_NAME']       = tds[6].firstElementChild.value		
		final_table_data[j] = table_data
	}
	
	full_data['observation']=final_table_data
	
	$.getJSON('/update_approve_deny_request', 
	{
		params_data : JSON.stringify(full_data)
	}, function(result) 
	{
		alert("EQUIPMENT DETAILS UPDATED");		
		window.location.reload();
	});
	
	
	
}




function thermal_submit(){
	
	
	var frame_list = document.getElementsByClassName("frame");
	var basic_details = {};
	
	if ($('#cycle_name').val()=="")
	{
		alert("Enter Cycle Name");
		return;
	}
	basic_details['cycle_name'] =$('#cycle_name').val();
	
	if ($('#started_on').val()=="")
	{
		alert("Cycle Start Time Required");
		return;
	}
	basic_details['started_on'] =$('#started_on').val();
	
	
	if ($('#cycle_start_time_duration').val()=="")
	{
		alert("Cycle start to Hold Duration Required");
		return;
	}
	basic_details['cycle_start_time_duration'] =$('#cycle_start_time_duration').val();
	
	if ($('#cycle_sterlization_duration').val()=="")
	{
		alert("Sterilization Hold Time Required");
		return;
	}
	basic_details['cycle_sterlization_duration'] =$('#cycle_sterlization_duration').val();
	
	if ($('#cycle_end_duration').val()=="")
	{
		alert("Hold End Time To Cycle End Time Required");
		return;
	}
	basic_details['cycle_end_duration'] =$('#cycle_end_duration').val();
	
	if ($('#interval_in_seconds').val()=="")
	{
		alert("Logging Interval Time Required");
		return;
	}
	basic_details['interval_in_seconds'] =$('#interval_in_seconds').val();
	
	if ($('#cycle_start_min').val()=="")
	{
		alert("Min. Temp At the Cycle Start Required");
		return;
	}
	basic_details['cycle_start_min'] =$('#cycle_start_min').val();
	
	if ($('#cycle_start_max').val()=="")
	{
		alert("Max. Temp At the Cycle Start Required");
		return;
	}
	basic_details['cycle_start_max'] =$('#cycle_start_max').val();
	
	if ($('#sterlization_min').val()=="")
	{
		alert("Min. Temp At the Hold Start Required");
		return;
	}
	basic_details['sterlization_min'] =$('#sterlization_min').val();
	
	if ($('#sterlization_max').val()=="")
	{
		alert("Max. Temp At the Hold Start Required");
		return;
	}
	basic_details['sterlization_max'] =$('#sterlization_max').val();
	
	if ($('#cycle_end_min').val()=="")
	{
		alert("Min. Temp At Cycle End Required");
		return;
	}
	basic_details['cycle_end_min'] =$('#cycle_end_min').val();
	
	if ($('#cycle_end_max').val()=="")
	{
		alert("Max. Temp At Cycle End Required");
		return;
	}
	basic_details['cycle_end_max'] =$('#cycle_end_max').val();
	
	if ($('#number_of_sensor').val()=="")
	{
		alert("Sensor Qty Required");
		return;
	}
	basic_details['number_of_sensor'] =$('#number_of_sensor').val();
		
	$.getJSON('/submit_thermal_report', 
	{
		params_data : JSON.stringify(basic_details)
	}, function(result) 
	{
		var link = document.createElement('a')
		link.href =result.file_path;
		link.download = result.file_name;
		link.dispatchEvent(new MouseEvent('click'));
		

		
	});
	
}



function view_expense()
{
	USERNAME = $('#USERNAME').val();
	STATUS = $('#STATUS').val();
	if ($('#USERNAME').val()=="")
	{
		alert("Please select USERNAME");
		return;
	}
	if ($('#STATUS').val()=="")
	{
		alert("Please select STATUS");
		return ;
	}
	
	basic_details={}
	basic_details['STATUS']        = $('#STATUS').val();
	basic_details['USERNAME']      = $('#USERNAME').val();
	basic_details['Expensetype']   = $('#Expensetype').val();
	basic_details['company_name']  = $('#company_name').val();
	
	$("#expense_submit_button").hide();	
	$.getJSON('/get_expense_sheet', 
	{
		params_data : JSON.stringify(basic_details)
	}, function(result) 
	{
		record_list =  result['expense_list']
		var approvedamount  = 0	
		var deniedamount    = 0	
		$('#EXPENSETABLE').empty();
		var header='<tr>\
				 <th>Request ID</th><th>Expense Type</th><th>Company Name</th>\
				 <th>Description</th><th>Amount Requested</th><th>Amount Approved</th><th>Date</th>\
				<th>Status</th></tr>'
		$('#EXPENSETABLE').append(header);
		for(var j = 0; j<record_list.length; j++)
		{	var company_name=record_list[j].company_name;
			var Expensetype=record_list[j].Expensetype;
			var Description=record_list[j].Description;
	        company_name = company_name.split(' ').join('\xa0');
			Expensetype  = Expensetype.split(' ').join('\xa0');
			Description  = Description.split(' ').join('\xa0');
	        
			if ( ($('#STATUS').val()=="APPROVED")  ||($('#STATUS').val()=="DENIED"))
			{	
			var temp = '<tr id="myTableRow" name="myTableRow">\
			<td><input type="text" name="request_id" value='+record_list[j].request_id+' class="textfield" disabled></td>\
			<td><input type="text" name="Expensetype" value='+Expensetype+' class="textfield" disabled></td>\
			<td><input type="text" name="company_name" value='+company_name+' class="textfield" disabled></td>\
			<td><input type="text" name="Description" value='+Description+' class="textfield" disabled></td>\
			<td><input type="text" name="Amount_requested" value='+record_list[j].Amount_requested+' class="textfield" disabled></td>\
			<td><input type="text" name="Amount_approved" value='+record_list[j].Amount_approved+' class="textfield" disabled ></td>\
			<td><input type="text" name="date" value='+record_list[j].date+' class="textfield" disabled></td>\
			<td>\
			<select class="textfield" name="STATUS" id="STATUS" style="width:100%" disabled>\
			<option value="">Select an option</option>\
			<option value="APPROVED">APPROVED</option>\
			<option value="DENIED">DENIED</option>\
			</select>\
			</td>\
			</tr>'
			approvedamount = parseFloat(approvedamount)+parseFloat(record_list[j].Amount_requested);
			deniedamount   = parseFloat(deniedamount)+parseFloat(record_list[j].Amount_approved);
			}
			else
			{
			$("#expense_submit_button").show();	
			var temp = '<tr id="myTableRow" name="myTableRow">\
			<td><input type="text" name="request_id" value='+record_list[j].request_id+' class="textfield" disabled></td>\
			<td><input type="text" name="Expensetype" value='+Expensetype+' class="textfield" disabled></td>\
			<td><input type="text" name="company_name" value='+company_name+' class="textfield" disabled></td>\
			<td><input type="text" name="Description" value='+Description+' class="textfield" disabled></td>\
			<td><input type="text" name="Amount_requested" value='+record_list[j].Amount_requested+' class="textfield" disabled></td>\
			<td><input type="text" name="Amount_approved" value='+record_list[j].Amount_requested+' class="textfield" ></td>\
			<td><input type="text" name="date" value='+record_list[j].date+' class="textfield" disabled></td>\
			<td>\
			<select class="textfield" name="STATUS" id="STATUS" style="width:100%">\
			<option value="APPROVED">APPROVE</option>\
			<option value="REQUESTED">REQUESTED</option>\
			<option value="DENIED">DENIED</option>\
			</select>\
			</td>\
			</tr>'
			approvedamount = parseFloat(approvedamount)+parseFloat(record_list[j].Amount_requested);
			deniedamount   = parseFloat(approvedamount)+parseFloat(record_list[j].Amount_requested);
			}
			$('#EXPENSETABLE tr:last').after(temp);		
		}		
		$('#approved').val(approvedamount)
		if ($('#STATUS').val()=="REQUESTED")
		{
			$('#declined').val(0)
		}
		else
		{
			$('#declined').val(parseFloat(approvedamount)-parseFloat(deniedamount))
		}
		
	});
	
}


function submit_expense()
{
	code_tbl = document.getElementsByClassName("code_tbl")[1]
	code_rows = code_tbl.rows	
	for(var j = 1; j<code_rows.length; j++)
	{
		tds = code_rows[j].children		
		if (tds[5].firstElementChild.value=="")
		{	
				alert("Filter Amount Approved cannot be blank in row : "+j);
				return;
		}	

        if (tds[7].firstElementChild.value=="")
		{	
				alert("Filter Status cannot be blank in row : "+j);
				return;
		}	
	}	
	
	var final_table_data = {};
    var full_data = {};	
	for(var j = 1; j<code_rows.length; j++)
	{
		tds = code_rows[j].children	
		var table_data = {};
		table_data['request_id']  = tds[0].firstElementChild.value 		
		table_data['Amount_approved'] = tds[5].firstElementChild.value 
		table_data['STATUS']  = tds[7].firstElementChild.value	
		final_table_data[j] = table_data
	}
	
	full_data['observation']=final_table_data	
	$.getJSON('/submit_expense', 
	{
		params_data : JSON.stringify(full_data)
	}, function(result) 
	{
		alert("Expense Request Updated");		
		window.location.reload();
	});
	
	
	
}

function submit_request_expense()
{
	code_tbl = document.getElementsByClassName("code_tbl")[0]
	code_rows = code_tbl.rows	
	for(var j = 1; j<code_rows.length; j++)
	{
		tds = code_rows[j].children		
		if (tds[0].firstElementChild.value=="")
		{	
				alert("Filter Expense Type cannot be blank in row : "+j);
				return;
		}	

        if (tds[1].firstElementChild.value=="")
		{	
				alert("Filter Company Name cannot be blank in row : "+j);
				return;
		}

		if (tds[2].firstElementChild.value=="")
		{	
				alert("Filter Description cannot be blank in row : "+j);
				return;
		}	
		
		if (tds[3].firstElementChild.value=="")
		{	
				alert("Filter Amount cannot be blank in row : "+j);
				return;
		}	
	}	
	
	var final_table_data = {};
    var full_data = {};	
	for(var j = 1; j<code_rows.length; j++)
	{
		tds = code_rows[j].children	
		var table_data = {};
		table_data['Expensetype']  = tds[0].firstElementChild.value 		
		table_data['company_name'] = tds[1].firstElementChild.value 
		table_data['Description']  = tds[2].firstElementChild.value	
		table_data['Amount']       = tds[3].firstElementChild.value		
		final_table_data[j] = table_data
	}
	
	full_data['observation']=final_table_data
	
	$.getJSON('/raise_expense', 
	{
		params_data : JSON.stringify(full_data)
	}, function(result) 
	{
		alert("Expense Request Raised");		
		window.location.reload();
	});
	
	
	
}


$('#EXPENSETABLE').on('change', 'input', function () 
{
    var req  = 0
    var appr  = 0
    var requested  =0
	var approvedamount =0
    code_tbl = document.getElementsByClassName("code_tbl")[1]
	code_rows = code_tbl.rows	
	for(var j = 1; j<code_rows.length; j++)
	{
		tds = code_rows[j].children	
        req  = tds[4].firstElementChild.value	
		appr = tds[5].firstElementChild.value
		requested = parseFloat(requested)+parseFloat(req);
		if (tds[0].firstElementChild.value=="")
		{	
				alert("Filter Expense Type cannot be blank in row : "+j);
				return;
		}	
		else
		{
			approvedamount   = parseFloat(approvedamount)+parseFloat(appr);
		}
	}	
	
	$('#approved').val(approvedamount)
	$('#declined').val(parseFloat(requested)-parseFloat(approvedamount))
	
	
	
});


function view_user_details()
{
	USERNAME = $('#USERNAME').val();
	if ($('#USERNAME').val()=="")
	{
		alert("Please select USERNAME");
		return;
	}	
	basic_details={}
	basic_details['USERNAME'] = $('#USERNAME').val();
	$.getJSON('/get_user_detail_by_userID_sheet', 
	{
		params_data : JSON.stringify(basic_details)
	}, function(result) 
	{
		var record_list =  result['user_list'][0]
		$('#USERTABLE').empty();
		var header='<tr>\
				 <th>Role</th><th>Username</th><th>First Name</th>\
				 <th>Last Name</th><th>Email ID</th><th>Status</th></tr>'
		$('#USERTABLE').append(header);
		
	
		var temp = '<tr id="myTableRow" name="myTableRow">\
		<td><select class="textfield" name="ROLE" id="ROLE" style="width:100%">'
		
		if (record_list.ROLE=="admin")
		{
			temp =temp +'<option value="admin" selected>Admin</option>'
			temp =temp +'<option value="analyst" >Service</option>'
			temp =temp +'<option value="operation" >Operation</option>'
			temp =temp+'</select></td>'
		}
		if (record_list.ROLE=="analyst")
		{
			temp =temp +'<option value="admin" >Admin</option>'
			temp =temp +'<option value="analyst" selected >Service</option>'
			temp =temp +'<option value="operation" >Operation</option>'
			temp =temp+'</select></td>'
		}
		if (record_list.ROLE=="operation")
		{
			temp =temp +'<option value="admin" >Admin</option>'
			temp =temp +'<option value="analyst" >Service</option>'
			temp =temp +'<option value="operation" selected>Operation</option>'
			temp =temp+'</select></td>'
		}
		
		temp=temp+'<td><input type="text" name="Username" id="Username" value='+record_list.USERNAME+' class="textfield" disabled></td>\
		<td><input type="text" name="FirstNAME" id="FirstNAME" value='+record_list.FNAME+' class="textfield" ></td>\
		<td><input type="text" name="LastNAME" id="LastNAME" value='+record_list.LNAME+' class="textfield" ></td>\
		<td><input type="text" name="emaild" id="emaild" value='+record_list.EMAILID+' class="textfield" ></td>\
		<td>\
		<select class="textfield" name="STATUS" id="STATUS" style="width:100%">\
		'	
		if (record_list.STATUS=="ACTIVE")
		{
			temp =temp +'<option value="ACTIVE" selected>ACTIVE</option>'
			temp =temp +'<option value="INACTIVE" >INACTIVE</option>'
		}
		else
		{
			temp =temp +'<option value="ACTIVE" >ACTIVE</option>'
			temp =temp +'<option value="INACTIVE" selected>INACTIVE</option>'
		}

		temp =temp+'</select></td></tr>'
		$('#USERTABLE tr:last').after(temp);		
				
		
		
	});
	
}


function update_user_details()
{
	if ($('#FirstNAME').val()=="")
	{
		alert("Please Enter First Name");
		return;
	}	
	if ($('#LastNAME').val()=="")
	{
		alert("Please Enter Lat Name");
		return;
	}
	
	basic_details={}
	basic_details['USERNAME']  = $('#USERNAME').val();
	basic_details['FirstNAME'] = $('#FirstNAME').val();
	basic_details['LastNAME']  = $('#LastNAME').val();
	basic_details['STATUS']    = $('#STATUS').val();
	basic_details['ROLE']      = $('#ROLE').val();
	basic_details['emaild']    = $('#emaild').val();
	$.getJSON('/submit_update_user_details', 
	{
		params_data : JSON.stringify(basic_details)
	}, function(result) 
	{
		alert("User Details Updated");		
				
		
		
	});
	
}

function exportdb()
{
	$.getJSON('/export_db', 
	{
		params_data : JSON.stringify("")
	}, function(result) 
	{
		var link = document.createElement('a')
		link.href =result.file_path;
		link.download = result.file_name;
		link.dispatchEvent(new MouseEvent('click'));		
	});
	
}





