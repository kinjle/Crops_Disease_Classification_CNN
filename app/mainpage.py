import streamlit as st
import requests
import os
import base64
from fpdf import FPDF

# Expanded remedies dictionary
disease_info = {
    "Apple Black Rot": {
        "description": "Black rot disease, caused by the fungus Botryosphaeria obtusa (Schwein), is concerning to homeowners with apple trees as part of their landscapes. All apple cultivars are susceptible to it, but it appears that McIntosh, Cortland, Empire and Northern Spy varieties are the preferred hosts. It seems that black rot is becoming more of a problem than usual. Normally, protectant apple scab programs would keep black rot in check. But, since incorporating other materials (like sterol inhibitors) that have no effect on these fungi, symptoms were more readily observed in the orchards throughout the state.",

        "symptoms": "Diseased limbs show symptoms that resemble fire blight. They appear as reddish-brown sunken areas with rough, cracked bark. The old cankers are dry and appear blistered, peeling and revealing black pimple-like, spore-carrying structures. Leaf lesions start as very small purple spots. As they grow larger, there is a brownish-tan center with darker margins and a purple outline that resemble a frog’s eye; this stage of disease is often referred to as frog-eye disease. Symptoms on the fruit appear at the calyx end as brown/rotted lesions. As the lesions enlarge, they form a number of concentric rings.",

        "causes": "Caused by the fungus Botryosphaeria obtusa.",

        "remedy": "To manage apple black rot effectively, focus on good sanitation practices and tree care. Start by pruning dead or diseased branches and removing all dried fruits and infected plant material, ensuring these are burned or buried to reduce spore sources. Be sure to remove any tree stumps, as they can harbor spores. Prune trees during colder months, such as February and March, when the fungus is inactive. Begin by removing dead branches and then shape the tree, allowing winter cuts to heal before spring. Maintain overall tree health by choosing suitable planting sites, selecting hardy cultivars, providing adequate water, and managing fire blight by removing affected limbs. While fungicide sprays are generally not necessary in Minnesota, consider them only if cultural practices fail. Products like Captan and sulfur can help control both black rot and apple scab but are not effective against branch infections."
    },

    "Apple Scab": {
        "description": "Apple scab is a fungal disease caused by Venturia inaequalis, primarily affecting apple and crabapple trees. It manifests as round, olive-green spots on leaves, which eventually turn dark brown to black, leading to premature leaf drop. Infected fruit may develop olive-green spots that turn brown and corky, and young fruit can become deformed and cracked. This disease thrives in moist conditions, making cultural practices and resistant varieties essential for management.",

        "symptoms": "Infected leaves show round, olive-green spots up to ½ inch across, which have a velvet-like texture and fringed borders. As the spots age, they turn dark brown to black, enlarging and merging together, often forming along the leaf veins. Affected leaves may yellow and drop by mid-summer. Infected fruit display olive-green spots that eventually turn brown and corky. Young infected fruit may become deformed and cracked as they grow.",

        "causes": "Apple scab is caused by the fungus Venturia Inaequalis",

        "remedy": "To manage apple scab in apples and crabapples, implement good cultural practices and choose disease-resistant varieties. Start by cleaning up fallen leaves in the fall to eliminate potential overwintering sites for the fungus; remove them before the first snowfall by burning, burying, or composting, or chop them with a mulching mower to aid decomposition. Proper planting and pruning are crucial, as the apple scab fungus thrives in moisture. Maintain an open canopy to promote airflow, allowing leaves to dry quickly. Avoid overcrowding plants by using the mature tree size for spacing, and prune branches to enhance air circulation. Additionally, remove upright suckers and water sprouts from the trunk and canopy to further reduce humidity and infection risk."
    },
    "Apple Healthy": {
        "description": "No disease present.",
        "symptoms": "No symptoms.",
        "causes": "N/A",
        "remedy": "No remedy needed."
    },

    "Corn Cercospora Spot-Gray Leaf Spot": {
        "description": "A fungal disease causing leaf spots.",
        
        "symptoms": "The disease first appears in the form of small, necrotic spots with halos. These usually expand to become rectangular lesions, about 1/8 inch wide by up to 2 inches to 3 inches long and gray to brown in appearance. Mature lesions usually have distinct parallel edges and appear opaque when put up to the light, but the lesions hybrids vary widely in shape and color. Symptoms can sometimes be confused with northern corn leaf spot, although gray leaf spot lesions are usually limited on the sides by veins.",

        "causes": "Caused by the fungus Cercospora zeae-maydis.",

        "remedy": "Key remedies for managing gray leaf spot include planting resistant hybrids, rotating crops with non-hosts, and managing residue by burying it to promote decomposition. Apply fungicides based on scouting, particularly if symptoms are present in at least half the plants."
    },

    "Corn Common Rust": {
        "description": "Corn common rust, caused by the fungus *Puccinia sorghi*, is a widespread disease affecting corn (maize) plants. It is characterized by the appearance of small, round, reddish-brown pustules on leaves, husks, and stalks. These pustules eventually rupture, releasing spores that can infect other plants. Common rust can significantly reduce photosynthesis, leading to stunted growth and decreased yields, especially in susceptible corn hybrids. The disease thrives in warm, humid conditions and can spread rapidly, making effective management strategies essential for maintaining healthy crops.",

        "symptoms": "Symptoms of corn common rust typically appear after silking and include small, round to elongated brown pustules on both leaf surfaces and other above-ground parts of the plant. As these pustules mature, they turn brown to black. In severe cases, affected leaves may yellow and die prematurely.",

        "causes": "Caused by the fungus Puccinia Sorghi.",

        "remedy": "The best management practice is to use resistant corn hybrids. Fungicides can also be beneficial, especially if applied early when few pustules have appeared on the leaves."
    },


    "Corn Northern Leaf Blight": {
        "description": "Corn northern leaf blight is a fungal disease caused by *Exserohilum turcicum* that primarily affects corn plants. It is characterized by elongated, grayish-green lesions on the leaves, which can grow up to several inches long. As the disease progresses, these lesions may turn brown and lead to premature leaf death. Northern leaf blight thrives in warm, humid conditions, and severe infections can significantly reduce photosynthesis, leading to decreased corn yields. Effective management strategies include crop rotation, planting resistant hybrids, and timely fungicide applications when necessary.",


        "symptoms": "Large, gray lesions on leaves.",

        "causes": "Caused by the fungus Exserohilum turcicum.",

        "remedy": "To manage northern corn leaf blight (NCLB), choose resistant hybrids, reduce corn residue through crop rotation and tillage, and plant timely. Consider fungicide applications based on disease risk factors, hybrid susceptibility, and weather conditions during the reproductive phase."
    },

    "Corn Healthy": {
        "description": "No disease present.",
        "symptoms": "No symptoms.",
        "causes": "N/A",
        "remedy": "No remedy needed."
    },

    "Potato Early Blight": {
        "description": "Early blight of potato is caused by the fungus, Alternaria solani, which can cause disease in potato, tomato, other members of the potato family, and some mustards. This disease, also known as target spot, rarely affects young, vigorously growing plants. It is found on older leaves first. Early blight is favored by warm temperatures and high humidity.",

        "symptoms": "Dark, target-like spots on leaves.",

        "causes": "Caused by the fungus Alternaria solani.",

        "remedy": "Varieties resistant to this disease are available. In general, late maturing varieties are more resistant than the earlier maturing varieties. Keep plants healthy; stressed plants are more predisposed to early blight. Avoid overhead irrigation. Do not dig tubers until they are fully mature in order to prevent damage. Do not use a field for potatoes that was used for potatoes or tomatoes the previous year. Keep this year’s field at least 225 to 450 yards away from last year’s field. Surround the field with wheat to keep wind-blown spores from entering. Use adequate nitrogen levels and low phosphorus levels to reduce disease severity. See current recommendations for chemical control measures."
    },

    "Potato Late Blight": {
        "description": "Late blight of potato is a serious disease caused by Phytophthora infestans. It affects potato, tomato and, occasionally, eggplant and other members of the potato family. Late blight is the worst potato disease. It was first reported in the 1830s in Europe and in the US. It is famous for being the cause of the 1840s Irish Potato Famine, when a million people starved and a million and a half people emigrated. Late blight continued to be a devastating problem until the 1880s when the first fungicide was discovered. In recent years, it has reemerged as a problem. It is favored by cool, moist weather and can kill plants within two weeks if conditions are right.",

        "symptoms": "White, fluffy fungal growth is present on the bottoms of leaves in moist weather. Leaf spots are not bordered by veins.",

        "causes": "Caused by the fungus Phytophthora infestans.",

        "remedy": "Use disease-free seed potatoes. Keep cull/compost piles away from potato growing areas. Destroy any volunteer potato plants. Keep tubers covered with soil throughout the season to prevent tuber infection. Remove infected tubers before storing to prevent the spread of disease in storage. Kill vines completely before harvest to avoid inoculation of the tubers during harvest. Resistant varieties are available, although some fungicides must still be applied to resistant cultivars. See current recommendations for chemical control measures."
    },
    "Potato Healthy": {
        "description": "No disease present.",
        "symptoms": "No symptoms.",
        "causes": "N/A",
        "remedy": "No remedy needed."
    }
}

def generate_pdf(uploaded_file, predicted_class, confidence, disease_data):
    # Save the uploaded file temporarily
    temp_image_path = f"temp_image_{uploaded_file.name}"
    
    with open(temp_image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="Disease Classification Report", ln=True, align="C")
    
    # Add image with margins
    pdf.image(temp_image_path, x=10, y=30, w=100)
    
    # Add details below the image with more spacing
    pdf.ln(150)  # Move down after the image for better spacing
    pdf.set_font("Arial", size=12)
    
    # Include the new information

    pdf.cell(200, 10, txt="Disease Classification Report", ln=True, align='C')
    pdf.multi_cell(0, 10, txt=f"Predicted Class: {predicted_class}")  
    pdf.multi_cell(0, 10, txt=f"Accuracy: {confidence:.2f}%")  
    pdf.multi_cell(0, 10, txt=f"Description: {disease_data['description']}")  
    pdf.multi_cell(0, 10, txt=f"Symptoms: {disease_data['symptoms']}")  
    pdf.multi_cell(0, 10, txt=f"Causes: {disease_data['causes']}") 
    pdf.multi_cell(0, 10, txt=f"Remedy: {disease_data['remedy']}")  
    
    # Save the PDF to a file
    pdf_output_path = f"{uploaded_file.name}_report.pdf"
    pdf.output(pdf_output_path)
    
    # Remove the temporary image file
    os.remove(temp_image_path)
    
    return pdf_output_path


# Function to create a download link for the PDF
def create_download_link(pdf_path):
    with open(pdf_path, "rb") as pdf_file:
        pdf_data = pdf_file.read()
    b64_pdf = base64.b64encode(pdf_data).decode('utf-8')
    href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="{os.path.basename(pdf_path)}">Download Report</a>'
    return href

# Main Streamlit app logic
st.title("Multiple Crops Disease Classification")
crops = ['Apple', 'Corn', 'Potato']
selected_crop = st.selectbox("Select a crop:", crops)

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption='Uploaded Image')

    # Define the API endpoint based on selected crop
    if selected_crop == 'Apple':
        api_url = 'http://localhost:8000/predictForApple'
    elif selected_crop == 'Corn':
        api_url = 'http://localhost:8000/predictForCorn'
    else:  # Potato
        api_url = 'http://localhost:8000/predictForPotato'

    # Make an API call
    files = {'file': uploaded_file.getvalue()}
    response = requests.post(api_url, files=files)

    # Display the predicted class and confidence
    if response.status_code == 200:
        result = response.json()
        
        predicted_class = f"{selected_crop} {result['predicted_class']}"  # Combine crop and predicted class
        confidence = result['accuracy'] * 100

        st.write(f"Predicted Class: {predicted_class}")
        st.write(f"Accuracy: {confidence:.2f}%")

        # Get disease data
        disease_data = disease_info.get(predicted_class, {
            "description": "No information available.",
            "symptoms": "N/A",
            "causes": "N/A",
            "remedy": "No remedy available for this disease."
        })
        
        st.write("Disease details will be included in the report.")

        # Generate PDF Report
        if st.button("Generate Report"):
            pdf_path = generate_pdf(uploaded_file, predicted_class, confidence, disease_data)
            download_link = create_download_link(pdf_path)
            st.markdown(download_link, unsafe_allow_html=True)
    else:
        st.write("Error: Could not retrieve prediction.")






















# import streamlit as st
# import requests
# import os
# import base64
# from fpdf import FPDF

# # Remedies dictionary
# remedies = {
#     "Apple Black Rot": "Remove infected fruit and leaves, apply fungicide.",
#     "Apple Scab": "Apply fungicide and prune affected branches.",
#     "Apple Healthy": "No remedy needed.",
#     "Corn Cercospora Spot-Gray Leaf Spot": "Rotate crops, apply fungicide.",
#     "Corn Common Rust": "Apply fungicide and plant resistant hybrids.",
#     "Corn Northern Leaf Blight": "Rotate crops and use resistant hybrids.",
#     "Corn Healthy": "No remedy needed.",
#     "Potato Early Blight": "Use disease-free seed, rotate crops, apply fungicide.",
#     "Potato Late Blight": "Remove infected plants, apply fungicide.",
#     "Potato Healthy": "No remedy needed."
# }

# def generate_pdf(uploaded_file, predicted_class, confidence, remedy):
#     # Save the uploaded file temporarily
#     temp_image_path = f"temp_image_{uploaded_file.name}"
    
#     with open(temp_image_path, "wb") as f:
#         f.write(uploaded_file.getbuffer())
    
#     # Create PDF
#     pdf = FPDF()
#     pdf.add_page()
    
#     # Title
#     pdf.set_font("Arial", "B", 16)
#     pdf.cell(200, 10, txt="Disease Classification Report", ln=True, align="C")
    
#     # Add image with margins
#     pdf.image(temp_image_path, x=10, y=30, w=100)
    
#     # Add details below the image with more spacing
#     pdf.ln(150)  # Move down after the image for better spacing
#     pdf.set_font("Arial", size=12)
#     pdf.cell(200, 10, txt=f"Predicted Class: {predicted_class}", ln=True)
#     pdf.cell(200, 10, txt=f"Accuracy: {confidence:.2f}%", ln=True)
#     pdf.cell(200, 10, txt=f"Remedy: {remedy}", ln=True)
    
#     # Save the PDF to a file
#     pdf_output_path = f"{uploaded_file.name}_report.pdf"
#     pdf.output(pdf_output_path)
    
#     # Remove the temporary image file
#     os.remove(temp_image_path)
    
#     return pdf_output_path


# # Function to create a download link for the PDF
# def create_download_link(pdf_path):
#     with open(pdf_path, "rb") as pdf_file:
#         pdf_data = pdf_file.read()
#     b64_pdf = base64.b64encode(pdf_data).decode('utf-8')
#     href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="{os.path.basename(pdf_path)}">Download Report</a>'
#     return href

# # Main Streamlit app logic
# st.title("Multiple Crops Disease Classification")
# crops = ['Apple', 'Corn', 'Potato']
# selected_crop = st.selectbox("Select a crop:", crops)

# uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# if uploaded_file is not None:
#     st.image(uploaded_file, caption='Uploaded Image')

#     # Define the API endpoint based on selected crop
#     if selected_crop == 'Apple':
#         api_url = 'http://localhost:8000/predictForApple'
#     elif selected_crop == 'Corn':
#         api_url = 'http://localhost:8000/predictForCorn'
#     else:  # Potato
#         api_url = 'http://localhost:8000/predictForPotato'

#     # Make an API call
#     files = {'file': uploaded_file.getvalue()}
#     response = requests.post(api_url, files=files)

#     # Display the predicted class and confidence
#     if response.status_code == 200:
#         result = response.json()
        
#         predicted_class = f"{selected_crop} {result['predicted_class']}"  # Combine crop and predicted class
#         confidence = result['accuracy'] * 100

#         st.write(f"Predicted Class: {predicted_class}")
#         st.write(f"Accuracy: {confidence:.2f}%")

#         # Remedy
#         remedy = remedies.get(predicted_class, "No remedy available for this disease.")
#         st.write(f"Remedy: {remedy}")

#         # Generate PDF Report
#         if st.button("Generate Report"):
#             pdf_path = generate_pdf(uploaded_file, predicted_class, confidence, remedy)
#             download_link = create_download_link(pdf_path)
#             st.markdown(download_link, unsafe_allow_html=True)
#     else:
#         st.write("Error: Could not retrieve prediction.")